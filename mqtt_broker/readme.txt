Set new username and password for mqtt broker with this command:

docker exec -it mosquitto mosquitto_passwd -b mosquitto/config/mosquitto.passwd <username> <password>
