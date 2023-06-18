<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">

  </a>

  <h3 align="center">trade-tools-api</h3>

  <p align="center">
    A Python/Flask Based API to allow me to analyse trading data. 
    <br />
    <br />
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

There are many trading dashboard tools out there, but none are as customizable as I'd like. This project is a still-in-development attempt to collate trading data from various personal accounts and allow me to call an API to pull whatever data I would like. 

Building an API gave me the ability to decouple the front and backend. For now I plan to keep the trading stats text message based with daily reports, but having an API ready allows me to consider building a reactive site to display the trading data. 
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This API was built in Python using Flask. It runs locally using gUnicorn WSGI, and hosted for a 'production' version using Heroku. 

Static scripts that analysed a database would not have worked for this project, as the trading accounts are run on various platforms, so having multiple instances of the application was a must.

Technologies:
<div align="center">
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" alt="Python" title="Python"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/183896132-54262f2e-6d98-41e3-8888-e40ab5a17326.png" alt="AWS" title="AWS"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/183896128-ec99105a-ec1a-4d85-b08b-1aa1620b2046.png" alt="MySQL" title="MySQL"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/192107854-765620d7-f909-4953-a6da-36e1ef69eea6.png" alt="HTTP" title="HTTP"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/183423775-2276e25d-d43d-4e58-890b-edbc88e915f7.png" alt="Flask" title="Flask"/></code>
</div>
<br>
Python Flask webserver which connects to MySQL database hosted with AWS.

POST requests to the api require an API key which is used to hash the request body so the server knows the request was from my trusted applications.




<p align="right">(<a href="#readme-top">back to top</a>)</p>
