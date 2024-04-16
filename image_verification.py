import hashlib
import img_hash_db

hashdatabase = img_hash_db.ImgDb()


# create a db to save past hashes


def verify_image(hash_val):  # TRUE FOR FINE FALSE FOR FAILED
    if hashdatabase.check_hash_exist(hash_val):
        print("failed")
        return False
    else:
        print("passed")
        hashdatabase.add_hash(hash_val)
        return True
