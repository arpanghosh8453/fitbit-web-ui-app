# **How to get Fitbit API Access Token**

  

## 1.  Method one : Official way
    

  

1.  Visit [this page](https://dev.fitbit.com/build/reference/web-api/developer-guide/getting-started/) and follow tutorial to create your own application
    
2.  Open [this page](https://dev.fitbit.com/build/reference/web-api/troubleshooting-guide/oauth2-tutorial/?clientEncodedId=23R3K5&redirectUri=https://localhost:8000/&applicationType=PERSONAL) and continue the process
    
3.  After you authorize your own application, you will get a ACCESS TOKEN and REFRESH TOKEN after following the whole process
    

  

##	  Method two : Quick way
    

  

1.  Open a tab in the browser and visit [https://dev.fitbit.com/login](https://dev.fitbit.com/login)
    
2.  Login if you are not logged in the current browser session
    
3.  Open [this page](https://dev.fitbit.com/build/reference/web-api/explore/) and click on the green Authorize button, select all and hit “Authorize” button below the dialog box, then hit close

![](https://lh5.googleusercontent.com/AZgvAQXZIV7K7kOwZOU0GqujkVoIaDjSy7OwtiK_DCeSciPQUF7scf9lZpJhKx1CKz0E9CHCKfYD-wtjU24EVUtFQIpUj6ZpZMSogBtPu_cDde015aDkUilrnx05cTRbT9yBPuq6N_6iCmUBHOekamI)
 
4.  Scroll down to the Devices section.
   
![](https://lh3.googleusercontent.com/Y3Ihrbx9NHsZx91sUyWgUlHror1oa4dZ_HNMfoRgPiENCpmYMH81YtFi_45hnPmIuRKd3kejpitFSS7Svv8EtYHxCi-sdWDfzJ-YJzcPicrj9Z73arTJWZZygV71m5EiAFE6N9h9Y7xpnM6Snn0uty8)  
  
  
  
  
  
  

5.  Click on “Try it out” and then click on “Execute” button
    

  
![](https://lh4.googleusercontent.com/YfW62QtSBaSSQvT1U_nKMtUQ8oCFweJvsgcW6J4CTN_oCMn0l8-Ye27LgNaMkale_tOWz5kW4agjCzAB64eoIJ_a1Z78_xztf9wDReRw_WEmq_5S5KZGdln8WuEnZcxEYNWW682r6IxfVAMGO8VwYYI)  
  
  
  
  
  
  
  
  
  
  

6.  You will see the API key in the curl command section. **Carefully copy only the part after the first line ( ending in Bearer )**
    

  

The “*curl -X GET "https://api.fitbit.com/1/user/-/devices.json" -H "accept: application/json" -H "authorization: Bearer*” **line is NOT a part of your API key.**

  

Also, avoid the quotation mark (“) at the end of the API key when you copy

  

I have blurred the API key part here in the above image.

It looks like a long continuous alphanumeric blob of characters without any space or meaningful word. Just copy the API key part.

  

**REMEMBER : Each API key has an hourly call limit and expires forever after 8 hours. One key will not work forever. If you use the same key in quick succession, you may hit the hourly rate limit.**
