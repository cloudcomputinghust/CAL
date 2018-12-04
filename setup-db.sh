echo Installing package
SUDO_PREFIX="sudo"

DOCKER_VERSION=$(docker -v)
if [ -z "$DOCKER_VERSION" ];
then
    sudo apt-get update
    sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable"

    sudo apt-get update
    sudo apt-get install -y docker-ce=17.03.2~ce-0~ubuntu-xenial
    sudo usermod -aG docker $(whoami)
fi

MYSQL_CONTAINER=$(docker ps -a | grep mysql | awk '{print $1}' )

if [ ! -z "$MYSQL_CONTAINER" ];
then
    $SUDO_PREFIX docker rm -f $MYSQL_CONTAINER
fi

sleep 3

started_time=$(date +%s%3N)
$SUDO_PREFIX docker run -idt --name some-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mysql:5.7
ended_time=$(date +%s%3N)

runtime=$((ended_time - started_time))

echo "Running time (ms) =" $runtime