from main import schema
from schema import SellerPost, BuyerPost, from_sql
import datetime


db = schema.db


def createPost(title, description, category, price, location, image, username, postType):
    time = datetime.datetime.now()
    if postType == "Seller":
        post = SellerPost(title=title, description=description, category=category, price=price, location=location, image=image, sellerName=username, time=time)
    if postType == "Buyer":
        post = BuyerPost(title=title, description=description, category=category, price=price, location=location, image=image, buyerName=username, time=time)
    try:
        db.session.add(post)
        db.session.commit()
        return post.postId
    except Exception as e:
        print e
        db.session.rollback()
        return None


def invalidSellerPost(postId):
    post = SellerPost.query.get(postId)
    try:
        post.valid = False
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def getPost(postId, postType):#
    if postType == "Seller":
        return searchSellerPosts(postId)
    if postType == "Buyer":
        return searchBuyerPosts(postId)
    return None


def deletePost(postType, postId):
    if postType == "Seller":
        return deleteSellerPositById(postId)
    if postType == "Buyer":
        return deleteBuyerPostById(postId)


def deleteSellerPositById(postId):
    try:
        SellerPost.query.filter_by(postId = postId).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def deleteBuyerPostById(postId):
    try:
        BuyerPost.query.filter_by(postId = postId).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def deleteSellerPostByUser(username):
    try:
        SellerPost.query.filter_by(sellerName = username).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def deleteBuyerPostByUser(username):
    try:
        BuyerPost.query.filter_by(buyerName = username).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def searchSellerPosts(postId=None, category=None, username=None):
    try:
        if postId is not None and category is None:
            post = SellerPost.query.get(postId)
            return schema.from_sql(post)
        else:
            query = SellerPost.query.filter_by(valid=True)
            if category is not None:
                query = query.filter_by(category=category)
            if username is not None:
                query = query.filter_by(sellerName=username)
            posts = []
            for post in query.all():
                posts.append(schema.from_sql(post))
            return posts
    except:
        return None


def searchBuyerPosts(postId=None, category=None, username=None):
    try:
        if postId is not None and category is None:
            post = BuyerPost.query.get(postId)
            return schema.from_sql(post)
        else:
            query = BuyerPost.query
            if category is not None:
                query = query.filter_by(category=category)
            if username is not None:
                query = query.filter_by(buyerName=username)
            posts = []
            for post in query.all():
                posts.append(schema.from_sql(post))
            return posts
    except:
        return None
