import os
import csv
import pandas as pd

class ReviewScraper(models.Manager):
    def new_review(self, store_name, user, title_review=None, body_review, rating, possible_rating, date_review,location=None, helpful=None, not_helpful=None, id_review=None):
        filepath = os.path.exists("reviews", f"{store_name}.csv")
        new_review_data = []
        # if the file exist
        if filepath:         
            with open(f'{store_name}.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    new_review_data.append(
                        {
                            "store_name": row[store_name],
                            "user": row[user],
                            "title_review": row[title_review],
                            "body_review": row[body_review],
                            "rating": row[rating],
                            "possible_rating": row[possible_rating],
                            "location": row[location],
                            "date_review": row[date_review],
                            "helpful": row[helpful],
                            "not_helpful": row[not_helpful],
                            "id_review": row[id_review]
                        }
                    )
            # Updating reviews
            _, filename = os.path.split(filepath)
            csvpath = os.path.join("review", filename)
            with open(csvpath, "w") as csvfile:
                fieldnames = ['store_name', 'user', 'title_review', 'body_review', 'rating', 'possible_rating', 'location', 'date_review', 'helpful', 'not_helpful', 'id_review']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(new_review_data)
        else:
            with open(f'{store_name}.csv', 'w') as csvfile:
                fieldnames = ['store_name', 'user', 'title_review', 'body_review', 'rating', 'possible_rating', 'location', 'date_review', 'helpful', 'not_helpful', 'id_review']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for row in writer:
                    new_review_data.append(
                        {
                            "store_name": row[store_name],
                            "user": row[user],
                            "title_review": row[title_review],
                            "body_review": row[body_review],
                            "rating": row[rating],
                            "possible_rating": row[possible_rating],
                            "location": row[location],
                            "date_review": row[date_review],
                            "helpful": row[helpful],
                            "not_helpful": row[not_helpful],
                            "id_review": row[id_review]
                        }
                    )
                writer.writeheader()
                writer.writerows(new_review_data)