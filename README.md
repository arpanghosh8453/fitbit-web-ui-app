# Fitbit Wellness Report Web UI

## Try it out

[Demo website on Render](https://fitbit-api-web-ui.onrender.com/) or [Self Hosted on my Server](https://fitbit-report.arpan.app/) (Use this if the Render page is down)

## What you will need

[How to get ACCESS TOKEN](https://github.com/arpanghosh8453/fitbit-web-ui-app/blob/main/help/GET_ACCESS_TOKEN.md)

## Preview of Data

![screenshot](https://github.com/arpanghosh8453/fitbit-web-ui-app/blob/main/help/Fitbit_Wellness_Report_Final_v2.jpg)

## Self-Hosting with Docker

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

## Support me 
If you love visualizing your long term data with this web app, please consider supporting me with a coffee ❤ if you can! You can view more detailed health statistics with this setup than paying a subscription fee to Fitbit, thanks to their REST API services. 

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/A0A84F3DP)
