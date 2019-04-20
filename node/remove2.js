"use strict";
/**
* This shows how to use standard Apollo client on Node.js
*/

global.WebSocket = require('ws');
require('es6-promise').polyfill();
require('isomorphic-fetch');

// Require exports file with endpoint and auth info
const aws_exports = require('./aws-exports').default;

// Require AppSync module
const AUTH_TYPE = require('aws-appsync/lib/link/auth-link').AUTH_TYPE;
const AWSAppSyncClient = require('aws-appsync').default;

//initiate user pool
const AmazonCognitoIdentity = require('amazon-cognito-identity-js');
const CognitoUserPool = AmazonCognitoIdentity.CognitoUserPool;
const request = require('request');
const jwkToPem = require('jwk-to-pem');
const jwt = require('jsonwebtoken');
global.fetch = require('node-fetch');

const poolData = {    
	UserPoolId : "us-east-1_KfNyfMR2A", // Your user pool id here    
	ClientId : "h8os0cpolbu01q7q2ip1prmc" // Your client id here
}; 

// If you want to use a jwtToken from Amazon Cognito identity:
//var jwtToken = 'xxxxxxxx'; 
const pool_region = aws_exports.REGION;
const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
//var myjwtToken;
function Login() {
    var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails({
        Username : 'bwlin0331',
        Password : 'bentley',
    });

    var userData = {
        Username : 'bwlin0331',
        Pool : userPool
    };
    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function (result) {
        	//myjwtToken = result.getAccessToken().getJwtToken();
            //console.log('access token + ' + result.getAccessToken().getJwtToken());
            //console.log('id token + ' + result.getIdToken().getJwtToken());
            //console.log('refresh token + ' + result.getRefreshToken().getToken());
            var accessToken = result.getAccessToken().getJwtToken();
            var idToken = result.getIdToken().getJwtToken();
            var today = new Date();
            var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
			var dd = String(today.getDate()).padStart(2, '0');		
			var yyyy = today.getFullYear();
			var HH = String(today.getHours()).padStart(2, '0');
			var mn = String(today.getMinutes()).padStart(2, '0');
			var ss = String(today.getSeconds()).padStart(2, '0');
			today = mm + '-' + dd + '-' + yyyy + ' ' + HH + ':' + mn + ':' + ss;
			var args = process.argv.slice(2);
			//console.log(args[0])
			// If you want to use AWS...
			const AWS = require('aws-sdk');
			
			const url = aws_exports.ENDPOINT;
			const region = aws_exports.REGION;
			const type = AUTH_TYPE.AMAZON_COGNITO_USER_POOLS;
            // Set up Apollo client
			const client = new AWSAppSyncClient({
			    url: url,
			    region: region,
			    auth: {
			        type: type,
			        jwtToken: accessToken,
			    },
			    disableOffline: true, 
			});
            // Import gql helper and craft a GraphQL query
			const gql = require('graphql-tag');
			const Query = gql(`
				query ListFoodItems{
				  listFoodItems(filter:{name:{
				  	 contains:"` + args[0] + `"
				  }}){
				    items{
				      id
				      date
				      name
				      description
				      quantity
				    }
				  }
				}`);
			var id, quantity, rquanity;

			client.hydrated().then(function (client) {
			    //Now run a mutation
			    client.query({ query: Query })
		    //client.query({ query: query, fetchPolicy: 'network-only' })   //Uncomment for AWS Lambda
		        .then(function logData(data) {

		            console.log('results of query: ', data);
		            //pdata = JSON.parse(data);
		            //console.log('item: ', data.data.listFoodItems.items);
		            if(data.data.listFoodItems.items.length != 0){

		            	id = data.data.listFoodItems.items[0].id;
		            	quantity = data.data.listFoodItems.items[0].quantity;
		            	rquanity = parseInt(args[1]);
		            	console.log(quantity);
		            	//console.log(typeof rquanity);

			            if(quantity == null || quantity <= rquanity){
			            	console.log("delete")
			            	client.mutate({ mutation: gql(`
								mutation DeleteFoodItem{
								  deleteFoodItem(input:{id : "` + id + `"}){
								    id 
								    date
								    name 
								    description 
								    quantity
								  }
								}
								`) })
						    //client.query({ query: query, fetchPolicy: 'network-only' })   //Uncomment for AWS Lambda
						        .then(function logData(data) {
						            console.log('results of mutation: ', data);
						        })
						        .catch(console.error);

					            

				        }else{
				        	console.log("update")
				        	client.mutate({ mutation: gql(`
								mutation UpdateFoodItem{
								  updateFoodItem(input:{id:"` + id + `", quantity:` + (quantity - args[1]) + `}){
								    id 
								    date
								    name 
								    description 
								    quantity
								  }
								}
								`) })
						    //client.query({ query: query, fetchPolicy: 'network-only' })   //Uncomment for AWS Lambda
						        .then(function logData(data) {
						            console.log('results of mutation: ', data);
						        })
						        .catch(console.error);
							
					     }
				      }


		        })
		        .catch(console.error);

			});

        },
        onFailure: function(err) {
            console.log(err);
        },

    });
}

Login()

