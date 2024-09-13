# Fitbit Wellness Report Web UI

[Live Demo website](https://fitbit-api-web-ui.onrender.com/) 

[Self Hosted Alternative website](https://fitbit-report.arpan.app/) 

[How to get ACCESS TOKEN](https://github.com/arpanghosh8453/fitbit-web-ui-app/blob/main/help/GET_ACCESS_TOKEN.md)

![screenshot](https://github.com/arpanghosh8453/fitbit-web-ui-app/blob/main/help/Fitbit_Wellness_Report_Final_v2.jpg)

# Self-Hosting with Docker

The following docker container `thisisarpanghosh/fitbit-report-app` is available for self hosting of this project. The Web app will be available on http://localhost:5000 with the configuration below. 

If you are interested in replacing the API token entering with a seamless login experience with Fitbit, Check out [PR#10](https://github.com/arpanghosh8453/fitbit-web-ui-app/pull/10) by [@Cronocide](https://github.com/Cronocide) available in the Fitbit-Oauth branch of this repository. 

```
services:
    fitbit-ui:
        image: 'thisisarpanghosh/fitbit-report-app:latest'
        container_name: 'fitbit-report-app'
        ports:
            - "5000:80"
        restart: unless-stopped
```

## Contributions

Special thanks to [@dipanghosh](https://github.com/dipanghosh) for his help and contribution towards the sleep schedule analysis part of the script and overall aesthetics suggestions. 
