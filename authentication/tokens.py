from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

# To send a confirmation email, we need to generate a  unique link 

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (
            text_type(user.pk)+text_type(timestamp)
        )
generate_token=TokenGenerator()

# PasswordResetTokenGenerator is generally used to reset the password 

# here , class TokenGenerator() inherited from the class PasswordResetTokenGenerator


'''
why six library necessary:
Common Use Cases: The library provides utilities for:
Handling differences in string types between Python 2 and Python 3.
Managing imports that have moved between versions.
Wrapping functions and iterators in a way that works in both Python versions.
Supporting metaclasses and exception handling syntax in a cross-compatible manner.

Token Generation: 
In your case, six is being used for token generation in Django. 
The token-related utilities that you're using may need six to handle 
string and byte encoding differences across Python versions.
'''

'''
In Django, a token is a unique string that is typically used to verify the identity 
of a user, particularly during sensitive actions like resetting passwords, 
email verification, or confirming account activation. 
The token ensures that the user who initiates an action (e.g., resetting a password) 
is the rightful owner of the account.

Why a Token is Necessary

Tokens are important for the following reasons:

Security: The token acts as a secure, one-time identifier that confirms 
that a user has permission to perform a particular action. 
For example, in password resets, it verifies that the person 
requesting the reset owns the account associated with the email.

Stateless Validation: Django can send a token to a user's email, 
and when the user clicks on the confirmation link, 
Django can validate the action without needing to store extra data in the database,
making the system more efficient.

Time Sensitivity: Tokens are often time-limited, meaning they expire after a certain 
period, adding an additional layer of security. 
For example, a token for password reset may only be valid for a couple of hours.


The TokenGenerator class inherits from Django's built-in PasswordResetTokenGenerator 
and is used to generate tokens for custom purposes like email verification
or account activation. 

PasswordResetTokenGenerator: 
This is a built-in Django class used to create secure, unique tokens.

_make_hash_value method: This is where the actual token string is created.
It's built using the user's primary key (user.pk) and a timestamp. 
By combining these values, Django generates a unique token for each user at a 
particular time.

Parameters:
user: The user object for which the token is being generated.
timestamp: A timestamp indicating when the token was generated.

generate_token: This is an instance of the TokenGenerator class 
that you can use to create and check tokens.

Hash Generation Logic:

text_type(user.pk): This converts the user's primary key (pk) to a string. 
text_type(timestamp): This converts the timestamp to a string.
The method then concatenates these two string values (user.pk and timestamp).

This hash value, which combines the user’s ID and a timestamp, will ensure 
the uniqueness of the token for each user and for each point in time. 
This way, even if two users request a token at the same time, 
their tokens will be different.
'''

'''
How It Works:

When you call generate_token.make_token(user), 
Django will use the _make_hash_value method to create a unique token based on the 
user’s primary key (user.pk) and the current timestamp.

This token is usually sent in an email for confirmation or reset purposes. 
The uniqueness of the token ensures that each user gets a personalized link and 
prevents issues like token reuse.

'''