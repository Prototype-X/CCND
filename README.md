# CCND
The collector of configurations for network devices
Support backup Cisco, Dlink, Edge-Core, Mikrotik, ELTEX

Cборщик конфигураций с свитчей и роутеров не шибко популярных вендоров.
Конечно же есть [rancid](https://www.shrubbery.net/rancid/) и [oxidized](https://github.com/ytti/oxidized) в последних версиях oxidized вроде как появилась поддержка Edge-Core и Dlink, не знаю на сколько она хороша. К сожалению не умею в Ruby, а то бы не делал эту поделку.

Что умеет данная утилита: 
1. бекапить конфиги в 32 процесса т.е. одновременно 32 железки
2. складывать конфиги в папку или зажимать их tar.gz
3. легко расширяется новым оборудованием template (если уметь чутка в питон)
4. Конфигурация хранится в [yaml](https://ru.wikipedia.org/wiki/YAML)

Требования:
1. Debian, Ubuntu
2. Python от 3.4
3. Настроенный рабочий tftp (предпочитаю [tftp-hpa](http://hh-pc.blogspot.com/2017/11/tftp-ubuntu.html))

    
    %YAML 1.2
    ---
    hostname:
      state: True
      group: group-name
      ip: 1.1.1.1
      port: 2222
      login: admin
      password: admin
      template: ssh-out-mtik
      storage: default
      profile: /dir/profile-name.yaml
      info: |
        New switch
        work fine
      
      
    hostname2:
      state: True
      group: group-name2
      ip: 1.1.1.2
      port: 2323
      login: admin
      password: admin
      template: telnet-tftp-dlink
      storage: tftp
      fetch: from_local_tftp
      profile: profile-name2.yaml
      info: |
        New switch
        work fine
      
      
...

Примечания: ELTEX бекапится начиная с версии 4.0.7.1, на более ранних версиях не работает