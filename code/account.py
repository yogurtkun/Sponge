from main import schema
from schema import User, from_sql
import message

db = schema.db

DELIMITER = ';'

def registerUser(username, email, password, zipcode):
    user = User(username=username, email=email, password=password, zipcode=zipcode)
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as e:
        print e
        db.session.rollback()
        return False


def loginUser(username, password):
    user = User.query.get(username)
    if user:
        if user.password == password:
            return 1
        return -1   # wrong password
    return 0    #user doesn't exist


def searchUser(username):
    user = User.query.get(username)
    if user:
        return from_sql(user)
    return None


def deleteUser(username):
    try:
        User.query.filter_by(username=username).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def addPost(username, postId, postType):
    user = User.query.get(username)
    if (postType == "Seller"):
        tmp = user.sellerPosts
        if tmp==None or len(tmp)==0:
            tmp = str(postId)
        else:
            tmp = tmp + DELIMITER + str(postId)
        try:
            user.sellerPosts = tmp
            db.session.commit()
            return True
        except Exception as e:
            print e
            db.session.rollback()
            return False
    if (postType == "Buyer"):
        tmp = user.buyerPosts
        if tmp==None or len(tmp)==0:
            tmp = str(postId)
        else:
            tmp = tmp + DELIMITER + str(postId)
        try:
            user.buyerPosts = tmp
            db.session.commit()
            return True
        except Exception as e:
            print e
            db.session.rollback()
            return False


def addFavorite(username, postId, postType):
    user = User.query.get(username)
    if (postType == "Seller"):
        tmp = user.favoriteSellerPosts
        if tmp==None or len(tmp)==0:
            tmp = str(postId)
        else:
            if str(postId) in tmp.split(DELIMITER):
                return True
            tmp = tmp + DELIMITER + str(postId)
        try:
            user.favoriteSellerPosts = tmp
            db.session.commit()
            return True
        except Exception as e:
            print e
            db.session.rollback()
            return False
    if (postType == "Buyer"):
        tmp = user.favoriteBuyerPosts
        if tmp==None or len(tmp)==0:
            tmp = str(postId)
        else:
            if str(postId) in tmp.split(DELIMITER):
                return True
            tmp = tmp + DELIMITER + str(postId)
        try:
            user.favoriteBuyerPosts = tmp
            db.session.commit()
            return True
        except Exception as e:
            print e
            db.session.rollback()
            return False


def deleteFavorite(username, postId, postType):
    user = User.query.get(username)
    if postType == "Seller":
        tmp = user.favoriteSellerPosts
        if tmp == None or len(tmp) == 0:
            return False
        favs = tmp.split(DELIMITER)
        favs = filter(lambda e : e != str(postId), favs)
        tmp = ""
        for e in favs:
            tmp += (e + DELIMITER)
        tmp = tmp[:-1]
        try:
            user.favoriteSellerPosts = tmp
            db.session.commit()
            return True
        except Exception as e:
            print e
            db.session.rollback()
            return False
    if postType == "Buyer":
        tmp = user.favoriteBuyerPosts
        if tmp == None or len(tmp) == 0:
            return False
        favs = tmp.split(DELIMITER)
        favs = filter(lambda e : e != str(postId), favs)
        tmp = ""
        for e in favs:
            tmp += (e + DELIMITER)
        tmp = tmp[:-1]
        try:
            user.favoriteBuyerPosts = tmp
            db.session.commit()
            return True
        except Exception as e:
            print e
            db.session.rollback()
            return False


def getFavorite(username):
    user = User.query.get(username)
    if user:
        user = from_sql(user)
        return user['favoriteSellerPosts'].split(DELIMITER), user['favoriteBuyerPosts'].split(DELIMITER)
    return [], []


def searchFavorite(username, postId, flag):
    user = User.query.get(username)
    if user:
        user = from_sql(user)
        if flag == "Seller":
            return str(postId) in user["favoriteSellerPosts"].split(DELIMITER)
        if flag == "Buyer":
            return str(postId) in user["favoriteBuyerPosts"].split(DELIMITER)
    return False


'''
When receiving a review, update rating
'''
def updateRating(username, rating):
    user = User.query.get(username)
    if user:
        tmp = user.rating
        c = user.ratingCount
        if tmp == None:
            tmp = rating
            c = 1
        else:
            tmp = (tmp * c + rating) / (c + 1.0)
            c = c + 1
        try:
            user.rating = tmp
            db.session.commit()
            user.ratingCount = c
            db.session.commit()
            return True
        except Exception as e:
            print e
            db.session.rollback()
            return False
    return False


def getRating(username):
    user = User.query.get(username)
    if user:
        return user.rating
    return None


'''
data: {attribute => value} for update
e.g. {'zipcode': '10027'}
'''
def updateUser(data, username):
    try:
        user = User.query.get(username)
        for k, v in data.items():
            setattr(user, k, v)
        db.session.commit()
        return schema.from_sql(user)
    except Exception as e:
        print e
        db.session.rollback()
        return None
