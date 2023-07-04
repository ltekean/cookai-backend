import hmac
import hashlib
import os
import time
import requests
import json
import urllib.request
from django.utils import timezone
from urllib.parse import urlencode
from articles.models import Ingredient, IngredientLink
from django.conf import settings
from ratelimiter import RateLimiter
from datetime import datetime


ACCESS_KEY = settings.COUPANG_ACCESS_KEY
SECRET_KEY = settings.COUPANG_SECRET_KEY


class CoupangManage:
    DOMAIN = "https://api-gateway.coupang.com"

    # HMAC서명 생성
    def generateHmac(self, method, url, secretKey, accessKey):
        path, *query = url.split("?")
        current_datetime = datetime.utcnow().strftime("%y%m%dT%H%M%SZ")
        message = current_datetime + method + path + (query[0] if query else "")
        signature = hmac.new(
            bytes(secretKey, "utf-8"), message.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(
            accessKey, current_datetime, signature
        )

    def get_productsdata(self, request_method, authorization, url):
        response = requests.request(
            method=request_method,
            url=url,
            headers={
                "Authorization": authorization,
                "Content-Type": "application/json;charset=UTF-8",
            },
        )
        retdata = json.dumps(response.json(), indent=4).encode("utf-8")
        jsondata = json.loads(retdata)
        data = jsondata["data"]

        productdata = data["productData"]

        return productdata

    def get_products_by_keyword(self, keyword, limit=10, subld="cookaicookai"):
        request_method = "GET"
        method = "GET"

        query = {"keyword": keyword, "limit": limit, "subId": subld}
        encoded_query = urlencode(query)

        # API 요청 URL
        request_url = (
            "/v2/providers/affiliate_open_api/apis/openapi/products/search?{}".format(
                encoded_query
            )
        )

        # HMAC 생성
        authorization = self.generateHmac(method, request_url, SECRET_KEY, ACCESS_KEY)

        # 요청 URL
        full_url = "{}{}".format(self.DOMAIN, request_url)

        # 상품 데이터 받기
        product_data = self.get_productsdata(request_method, authorization, full_url)

        # 딕셔너리 생성
        products = [
            {
                "product_url": product["productUrl"],
                "product_image_url": product["productImage"],
            }
            for product in product_data
        ]

        return products


# 전역 변수로 RateLimiter 객체 생성 (60초에 50회 제한)
coupang_api_limiter = RateLimiter(max_calls=50, period=60)


def save_coupang_links_to_ingredient_links(ingredient_name):
    # CoupangManage 객체 생성
    coupang_api = CoupangManage()

    # ratelimiter 적용하여 키워드를 기반으로 상품 정보 검색
    with coupang_api_limiter:
        product_links = coupang_api.get_products_by_keyword(ingredient_name, 10)

    # Ingredient DB에서 Ingredient_name 찾기
    try:
        ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)
    except Ingredient.DoesNotExist:
        print(f"{ingredient_name} 은(는) 데이터베이스에 없습니다.")
        return

    # 기존에 저장된 5일 전의 IngredientLinks 삭제
    old_links = IngredientLink.objects.filter(
        ingredient=ingredient,
        created_at__lt=timezone.now() - timezone.timedelta(days=5),
    )
    old_links.delete()

    for link_data in product_links:
        link = link_data["product_url"]
        link_img = link_data["product_image_url"]

        # 생성된 link 와 link_img를 IngredientLink DB에 저장
        ingredient_link = IngredientLink(
            ingredient=ingredient, link=link, link_img=link_img
        )
        ingredient_link.save()
        ingredient.save()

    # 모든 링크가 저장된 후서야 Ingredient의 updated_at을 업데이트
    ingredient.update_timestamp()


def update_ingredient_links(interval_days=3):
    new_ingredients = Ingredient.objects.filter(
        updated_at__isnull=True
    ) | Ingredient.objects.filter(
        updated_at__lt=timezone.now() - timezone.timedelta(days=interval_days)
    )

    for ingredient in new_ingredients:
        ingredient_name = ingredient.ingredient_name
        with coupang_api_limiter:
            save_coupang_links_to_ingredient_links(ingredient_name)
        ingredient.updated_at = timezone.now()
        ingredient.save()
    else:
        print("coupang")
