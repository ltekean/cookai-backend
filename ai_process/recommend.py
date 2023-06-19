# user - article table 만들어야하는데
from articles.models import Article
from users.models import User
from django_pandas.io import read_frame
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scipy.sparse.linalg import svds


def recommend_movies(
    df_svd_preds: pd.DataFrame,
    user_id,
    ori_movies_df,
    ori_ratings_df,
    num_recommendations=1,
):
    # 현재는 index로 적용이 되어있으므로 user_id - 1을 해야함.
    user_row_number = user_id - 1

    # 최종적으로 만든 pred_df에서 사용자 index에 따라 영화 데이터 정렬 -> 영화 평점이 높은 순으로 정렬 됌
    sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(
        ascending=False
    )

    # 원본 평점 데이터에서 user id에 해당하는 데이터를 뽑아낸다.
    user_data = ori_ratings_df[ori_ratings_df.userId == user_id]

    # 위에서 뽑은 user_data와 원본 영화 데이터를 합친다.
    user_history = user_data.merge(ori_movies_df, on="article").sort_values(
        ["score"], ascending=False
    )

    # 원본 영화 데이터에서 사용자가 본 영화 데이터를 제외한 데이터를 추출
    recommendations = ori_movies_df[
        ~ori_movies_df["article"].isin(user_history["article"])
    ]
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


def foo(user_id):
    users = User.objects.prefetch_related("likes").values("pk", "likes__pk")
    # Create the DataFrame
    df = read_frame(users, fieldnames=["pk", "likes"])
    df["score"] = 2
    df.columns = [{"pk": "pk", "likes": "article"}]
    users = User.objects.prefetch_related("bookmarks").values("pk", "bookmarks__pk")

    df2 = read_frame(
        User.objects.all().select_related("bookmarks"),
        fieldnames=["pk", "bookmarks"],
    )
    df2["score"] = 4
    df2.columns = [{"pk": "pk", "bookmarks": "article"}]
    df = pd.concat([df, df2], ignore_index=True)

    # pvt = pd.pivot_table(
    #     df, index=["pk", "article"], values="score_", aggfunc="sum"
    # ).fillna(0)
    pvt = pd.pivot_table(
        df, values="score", index=["pk"], columns=["article"], aggfunc=np.sum
    ).fillna(0)
    #########
    # pvt = pvt.transpose()
    # sim = cosine_similarity(pvt, pvt)

    # sim_df = pd.DataFrame(data = sim, index = pvt.index, columns = pvt.index)

    # matrix는 pivot_table 값을 numpy matrix로 만든 것
    matrix = pvt.values

    # user_ratings_mean은 사용자의 평균 score
    user_ratings_mean = np.mean(matrix, axis=1)

    # R_user_mean : 사용자-article에 대해 사용자 평균 평점을 뺀 것.
    matrix_user_mean = matrix - user_ratings_mean.reshape(-1, 1)
    u, sigma, vt = svds(matrix_user_mean, k=12)
    sigma = np.diag(sigma)
    svd_user_predicted_ratings = np.dot(
        np.dot(u, sigma), vt
    ) + user_ratings_mean.reshape(-1, 1)
    df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns=pvt.columns)
    df_articles = Article.objects.all()
    df_articles = read_frame(df_articles, fieldnames=["pk"])
    df_articles.columns = [{"pk": "article"}]
    df = df.groupby(["pk", "article"]).sum()
    already_rated, predictions = recommend_movies(
        df_svd_preds, user_id, df_articles, df, 1
    )
    return list(predictions["article"])
