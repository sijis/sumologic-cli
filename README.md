README
============

Sumologic is a cloud management log solution. This project is for a sumologic 
search client which will allow to do queries from the cli.

Sumologic API details are located on [their wiki](https://github.com/SumoLogic/sumo-api-doc/wiki/search-api)


API PASSWORD
--------------------
Since we use SAML to authenticate to Sumologic, we have to do the following
to get an API account:

- Login with SAML credentials
- Click on "Forgot Your Password"
- Follow the details in the email to change the password (this will be the
  API password)
- SAML credentials aren't affected by this process

Source: http://support.sumologic.com/tickets/1523

