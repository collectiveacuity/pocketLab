# System Architecture

## Layers
- databases
- systems
- clients (high-level)
- clients (low-level)
- commands
- handlers
- interfaces
- channel

## Client (Low-Level)
- direct interaction with database & system
- method nomenclature matches best practices of interpreters
- exceptions meant for module developer (not user)
- first-party services
- eg. loggingClient, localhostClient, boto3

## Client (High-Level)
- middleware between commands and low-level clients
- method nomenclature matches commands
- translates command details into low-level routines
- exceptions meant to pass through to handler
- third-party services
- eg. registryClient, dockerClient, awsClient

## Command
- coordinates interfaces, high level clients and handler
- method nomenclature represents scope of service
- translates input from interface into action & interface output
- sends exceptions, success, input events to handler
- high fault tolerant
- recursively true
- eg. start, stop, add, remove, list

## Handler
- middleware between service and user or data
- interprets observations and events throughout process
- handles all exceptions, notifications, inputs
- high fault tolerant
- recursively true
- intelligent
- eg. labBot, labBotJr

## Interface
- direct interaction with user and sensors
- method nomenclature matches best practices of interface type
- coordinates a variety of channels
- exceptions meant for module developer (not user)
- eg. cli, flask, chat

## Channel
- transmission method between user or data and interface
- method nomenclature dictated by third-party terms
- exceptions raised need to be interpreted by interface
- eg. twilio, terminal, api, browser