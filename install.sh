if [ "$1" = "install" ]; then
	echo -e "\e[93m[!]\e[36mInstalling required packages...\e[0m"
	apt-get update && apt-get upgrade
	apt-get install python3
	pip3 install bs4 pandas requests geoip2 colorama
elif [ "$1" = "update" ]; then
	echo -e "\e[93m[!]\e[36mFetching newest repository...\e[0m"
	git pull
	if [ $? -eq 0 ]; then
		echo -e "\e[93m[√]\e[32mRepository successfully updated\e[0m"
	else
		echo -e "\e[93m[X]\e[31mRepository was not updated. Please check your internet connection\e[0m"
	fi
else
	echo -e "Usage:\n\t./install.sh install (install dependencies)\n\t./install.sh update (update repository)\n"
fi