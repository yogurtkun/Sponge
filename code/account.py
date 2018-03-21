from main import schema
from schema import User, from_sql

db = schema.db


def registerUser(username, email, password, zipcode):
    user = User(username=username, email=email, password=password, zipcode=zipcode)
    try: 
        db.session.add(user)
        db.session.commit()
        return True
    except:
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
            tmp = tmp + ";" + str(postId)
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
            tmp = tmp + ";" + str(postId)
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
            tmp = tmp + ";" + str(postId)
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
            tmp = tmp + ";" + str(postId)
        try:
            user.favoriteBuyerPosts = tmp
            db.session.commit()
            return True
        except Exception as e:
            print e
            db.session.rollback()
            return False


'''
data: {attribute => value} for update
e.g. {'zipcode': '10027'}
'''
def updateUser(data, username):
    try:
        user = User.query.get(username)
        for k, v in data.items():
            setattr(user, k, v)
        return schema.from_sql(user)
    except Exception as e:
        print e
        db.session.rollback()
        return None