import hmac
import hashlib
import os
import time
import requests
import json
import urllib.request
import secrets
from django.utils import timezone
from urllib.parse import urlencode
from articles.models import Ingredient, IngredientLink
from django.conf import settings


ACCESS_KEY = settings.COUPANG_ACCESS_KEY
SECRET_KEY = settings.COUPANG_SECRET_KEY


class coupangMgr:
    DOMAIN = "https://api-gateway.coupang.com"

    # HMAC서명 생성
    def generateHmac(self, method, url, secretKey, accessKey):
        path, *query = url.split("?")
        os.environ["TZ"] = "GMT+0"
        datetime = time.strftime("%y%m%d") + "T" + time.strftime("%H%M%S") + "Z"
        message = datetime + method + path + (query[0] if query else "")
        signature = hmac.new(
            bytes(secretKey, "utf-8"), message.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(
            accessKey, datetime, signature
        )

    def get_productsdata(self, request_method, authorization, keyword, limit):
        URL = (
            "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword="
            + urllib.parse.quote(keyword)
            + "&limit="
            + str(limit)
        )
        url = "{}{}".format(self.DOMAIN, URL)

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

    def get_products_by_keyword(self, keyword, limit=10):
        request_method = "GET"
        method = "GET"

        query = {"keyword": keyword, "limit": limit}
        encoded_query = urlencode(query)

        request_url = (
            "/v2/providers/affiliate_open_api/apis/openapi/products/search?{}".format(
                encoded_query
            )
        )

        authorization = self.generateHmac(method, request_url, SECRET_KEY, ACCESS_KEY)
        product_data = self.get_productsdata(
            request_method, authorization, keyword, limit
        )

        products = [
            {
                "product_url": product["productUrl"],
                "product_image_url": product["productImage"],
            }
            for product in product_data
        ]

        return products


def save_coupang_links_to_ingredient_links(ingredient_name):
    # coupangMgr 객체 생성
    coupang_api = coupangMgr()

    # 키워드를 기반으로 상품 정보검색
    product_links = coupang_api.get_products_by_keyword(ingredient_name, 10)

    # Ingredient DB에서 Ingredient_name 찾기
    try:
        ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)
    except Ingredient.DoesNotExist:
        print(f"{ingredient_name} 은(는) 데이터베이스에 없습니다.")
        return

    for link_data in product_links:
        link = link_data["product_url"]
        link_img = link_data["product_image_url"]

        # 생성된 link 와 link_img를 IngredientLink DB에 저장
        ingredient_link = IngredientLink(
            ingredient=ingredient, link=link, link_img=link_img
        )
        ingredient_link.save()


def update_ingredient_links(limit_per_minute=50, interval_days=1):
    new_ingredients = Ingredient.objects.filter(
        updated_at__isnull=True
    ) | Ingredient.objects.filter(
        updated_at__lt=timezone.now() - timezone.timedelta(days=interval_days)
    )

    for index, ingredient in enumerate(new_ingredients):
        if index < limit_per_minute * 24 * 60:
            ingredient_name = ingredient.ingredient_name
            save_coupang_links_to_ingredient_links(ingredient_name)
            ingredient.updated_at = timezone.now()
            ingredient.save()
        else:
            break
    else:
        print("coupang")
