# CCND
The collector of configurations for network devices
Support backup Cisco, Dlink, Edge-Core, Mikrotik, ELTEX

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

