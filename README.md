# cooldb

This is a simple wrapper for python's sqlite3 API\
__DISCLAIMER!!:__
This library is not intended to be used in production environments because it **IS NOT** protected against SQL
injection.

## 1. Explanation

This is a small project written in pure python. It abviously doesn't support all teh SQL functions but the basics are
covered.

## 2. Examples

Basic setup:

```py
from cooldb import Session

sess = Session('your db name')
sess.create_table('table name')

# create some data
sess.save('the table name', [your values here])
sess.update('the table name', {'some column name here': value}, {'your search criteria': value})
sess.delete('the table name', {'your search criteria': value})

# select and output some data
selection = sess.select('the table name', 10, {'your search criteria': value})

# close the connection to the database
sess.close()  # gets executed when something like 'del sess' is called
```

## 3. Future

At the moment I don't know if I will add more features. If you want to see more features please fork this repo und
create pull requests or just create an issue with the feature request tag.
PS: Maybe I will add an async version that uses aiosqlite but let's see ;)

# CHEERS