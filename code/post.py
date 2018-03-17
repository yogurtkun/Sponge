from main import schema
from schema import SellerPost, BuyerPost, from_sql
import datetime


db = schema.db


def createPost(title, description, category, price, location, image, username, seller, buyer):
    time = datetime.datetime.now()
    if seller:
        post = SellerPost(title=title, description=description, category=category, price=price, location=location, image=image, sellerName=username, time=time)
    if buyer:
        post = BuyerPost(title=title, description=description, category=category, price=price, location=location, image=image, buyerName=username, time=time)      
    try:
        db.session.add(post)
        db.session.commit()
        return post.postId
    except Exception as e:
        print e
        db.session.rollback()
        return None


def getPost(postId, seller, buyer):
    if seller:
        return searchSellerPosts(postId)
    if buyer:
        return searchBuyerPosts(postId)
    return None


def searchSellerPosts(postId=None):
    print "get seller post ", postId
    try:
        if postId is None:
            #   return all the sell posts
            #   not support paging
            posts = []
            for post in SellerPost.query.all():
                posts.append(from_sql(post))
            return posts
        else:
            post = SellerPost.query.get(postId)
            return from_sql(post)
    except Exception as e:
        print e
        return None


def searchBuyerPosts(postId=None):
    print "get buyer post ", postId
    try:
        if postId is None:
            #   return all the sell posts
            #   not support paging
            posts = []
            for post in BuyerPost.query.all():
                posts.append(from_sql(post))
            return posts
        else:
            post = BuyerPost.query.get(postId)
            return from_sql(post)
    except Exception as e:
        print e
        return None


def deleteSellerPostById(postId):
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
        
        
def searchSellerPosts(postId=None, category=None):
    try:
        if postId is not None and category is None:
            post = SellerPost.query.get(postId)
            return schema.from_sql(post)
        else:
            query = SellerPost.query
            if category is not None:
                query = query.filter_by(category=category)
            posts = []
            for post in query.all():
                posts.append(schema.from_sql(post))
            return posts
    except:
        return None


def searchBuyerPosts(postId=None, category=None):
    try:
        if postId is not None and category is None:
            post = BuyerPost.query.get(postId)
            return schema.from_sql(post)
        else:
            query = BuyerPost.query
            if category is not None:
                query = query.filter_by(category=category)
            posts = []
            for post in BuyerPost.query.filter_by(category=category).all():
                posts.append(schema.from_sql(post))
            return posts
    except:
        return None