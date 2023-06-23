# user - article table 만들어야하는데
from articles.models import Article
from users.models import User, Fridge
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scipy.sparse.linalg import svds
from sklearn.feature_extraction.text import TfidfVectorizer


def recommend_by_collabo(
    df_svd_preds: pd.DataFrame,
    user_id,
    ori_article_df,
    ori_ratings_df,
    num_recommendations=1,
):
    # 현재는 index로 적용이 되어있으므로 user_id - 1을 해야함.
    user_row_number = user_id - 1

    # 최종적으로 만든 pred_df에서 사용자 index맞는 아티클 데이터를 예상평점이 높은 순으로 정렬 됌
    sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(
        ascending=False
    )
    # 원본 평점 데이터에서 user id에 해당하는 데이터를 뽑아낸다.
    user_data = ori_ratings_df[ori_ratings_df["pk"] == user_id]
    # 위에서 뽑은 user_data와 원본 영화 데이터를 합친다.
    user_history = user_data.merge(ori_article_df, on="article").sort_values(
        ["score"], ascending=False
    )
    # 원본 아티클 데이터에서 사용자가 평가한 아티클 제외한 데이터를 추출
    recommendations = ori_article_df[
        ~ori_article_df["article"].isin(user_history["article"])
    ]
    recommendations = recommendations.loc[recommendations.author != user_id, :]
    # 사용자의 영화 평점이 높은 순으로 정렬된 데이터와 위 recommendations을 합친다.
    recommendations = recommendations.merge(
        pd.DataFrame(sorted_user_predictions).reset_index(), on="article"
    )
    # 컬럼 이름 바꾸고 정렬해서 return
    recommendations = (
        recommendations.rename(columns={user_row_number: "Predictions"})
        .sort_values("Predictions", ascending=False)
        .iloc[:num_recommendations, :]
    )
    return user_history, recommendations


def collaborative_filtering(user_id):
    """ """
    print("coll")
    users = User.objects.prefetch_related("likes").values("pk", "likes__pk")
    # Create the DataFrame
    df = pd.DataFrame(list(users))
    df.columns = ["pk", "article"]
    df["score"] = 2 * df["article"] / df["article"]
    users = User.objects.prefetch_related("bookmarks").values("pk", "bookmarks__pk")
    users2 = User.objects.prefetch_related("bookmarks").values("pk", "bookmarks__pk")
    df2 = pd.DataFrame(list(users2))
    df2.columns = ["pk", "article"]
    df2["score"] = 4 * df2["article"] / df2["article"]
    df = pd.concat([df, df2], ignore_index=True)
    articles = Article.objects.all().values("pk", "author")
    df3 = pd.DataFrame(list(articles))
    df3.columns = ["article", "author"]
    df = df.merge(right=df3, how="outer", on="article")
    unique_pk = df["pk"].dropna().unique()
    pvt = df.pivot_table(
        values="score",
        index=["pk"],
        columns=["article"],
        dropna=False,
        fill_value=0,
        aggfunc=np.sum,
    )
    pvt = pvt.reindex(unique_pk, fill_value=0).sort_index()
    matrix = pvt.values

    # user_ratings_mean은 사용자의 평균 score
    user_ratings_mean = np.mean(matrix, axis=1)

    # R_user_mean : 사용자-article에 대해 사용자 평균 평점을 뺀 것.
    matrix_user_mean = matrix - user_ratings_mean.reshape(-1, 1)
    k = min(matrix_user_mean.shape) - 1
    k = min(k, 12)
    u, sigma, vt = svds(matrix_user_mean, k=k)
    sigma = np.diag(sigma)
    svd_user_predicted_ratings = np.dot(
        np.dot(u, sigma), vt
    ) + user_ratings_mean.reshape(-1, 1)
    df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns=pvt.columns)
    df = df.groupby(["pk", "article"]).sum()
    df = df.reset_index()
    already_rated, predictions = recommend_by_collabo(
        df_svd_preds, user_id, df3, df, 10
    )
    ret = {
        pk: score
        for pk, score in zip(predictions["article"], predictions["Predictions"])
    }
    return list(predictions["article"]), ret


def queryset_to_str(query):
    try:
        list_ = [str(q) for q in list(query)]
        return " ".join(list_)
    except:
        return str(query)


def recommend_by_ingredient(matrix, items, k=10):
    recom_idx = (
        matrix.loc[:, 0].values.reshape(1, -1).argsort()[:, ::-1].flatten()[1 : k + 1]
    )
    recom_article = items.iloc[recom_idx, :].pk.values
    scores = []
    scores = [matrix.loc[i, 0] for i in recom_article]
    d = {
        "pk": recom_article,
        "score": scores,
    }
    return pd.DataFrame(d)


def content_base(user_id):
    print("cont")
    articles = Article.objects.exclude(author_id=user_id).values(
        "pk", "recipeingredient__ingredient"
    )

    df = (
        pd.DataFrame(list(articles))
        .groupby("pk")
        .aggregate({"recipeingredient__ingredient": queryset_to_str})
        .reset_index()
    )
    df.columns = ["pk", "ingredient"]
    fridge = Fridge.objects.filter(user_id=user_id).values("ingredient")

    df.loc[len(df.index)] = [0, queryset_to_str(fridge)]
    tfidf_vector = TfidfVectorizer()
    tfidf_matrix = tfidf_vector.fit_transform(df["ingredient"]).toarray()
    tfidf_matrix_feature = tfidf_vector.get_feature_names_out()
    tfidf_matrix = (
        pd.DataFrame(
            tfidf_matrix, columns=tfidf_matrix_feature, index=df["pk"]
        ).sort_index()
        # .reset_index()
    )
    print(tfidf_matrix)
    my_vector = list(tfidf_matrix.loc[0, :])
    list_ = []
    dict_ = {}

    cosine_sim = cosine_similarity(tfidf_matrix, [my_vector])
    dict_ = {
        key: value[0] for value, key in zip(cosine_sim[1:], tfidf_matrix.index[1:])
    }
    print(dict_)
    return [k for k in dict_.keys()][:10], dict_
