README
============

Sumologic is a cloud management log solution. This project is for a sumologic 
search client which will allow to do queries from the cli.

Sumologic API details are located on [their wiki](https://github.com/SumoLogic/sumo-api-doc/wiki/search-api)


API PASSWORD
--------------------
Since we use SAML to authenticate to Sumologic, we have to do the following
to get an API account:

"Currently the API is not authenticated against your SAML credentials, you will
need to use the direct Sumo Logic authentication for the API queries. When your
account was created in Sumo Logic you may have received a welcome message with
these Sumo Logic credentials, however if you did not receive this you should be
able to use the "Forgot Your Password?" link located on the login page to have
a new one sent to you. When prompted enter your same email address and select
OK. A new temporary password will then be sent to you by email. Once you have
logged in using the temporary password and set a new Sumo Logic password you
should be able to use those credentials for access to the API. Your SAML
credentials will continue to work even after resetting this password."

Source: http://support.sumologic.com/tickets/1523

