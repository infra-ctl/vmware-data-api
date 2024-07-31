include .env 
export .EXPORT_ALL_VARIABLES

# variables that can be defined by the user
IMAGE_NAME = vmware-data-api
CONTAINER_NAME = vmware-data-api-container
LOGS_FOLDER = /var/vmw/logs

# input vCenter credentials 
install:
	docker build --no-cache -t $(IMAGE_NAME) .
	docker run --name $(CONTAINER_NAME) -e VCENTER_IP=$(VCENTER_IP) -e VCENTER_USERNAME=$(VCENTER_USERNAME) -e VCENTER_PASSWORD=$(VCENTER_PASSWORD) -e GSHEET_ID=$(GSHEET_ID) -e GSHEET_NAME=$(GSHEET_NAME) -e GSHEET_KEY_PATH=$(GSHEET_KEY_PATH) -v $(LOGS_FOLDER):/app/.logs $(IMAGE_NAME)
	echo "0 20 * * * docker start $(CONTAINER_NAME)" >> /etc/crontab

remove:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
	docker rmi $(IMAGE_NAME)
	sed -i '/$(CONTAINER_NAME)/d' /etc/crontab
