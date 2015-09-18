# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.provider :virtualbox do |vb, override|
    override.vm.box = "ubuntu/trusty64"
    override.vm.box_url =  "https://vagrantcloud.com/ubuntu/boxes/trusty64/versions/14.04/providers/virtualbox.box"
    override.vm.synced_folder ".", "/vagrant",type: "rsync"
    override.ssh.username = "vagrant"
    vb.customize ["modifyvm", :id, "--cpus", "1"]
    vb.customize ["modifyvm", :id, "--memory", "512"]
  end

  config.vm.provider :aws do |aws, override|
    override.vm.box = "Restparql"
    override.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"
    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = "#{ENV['AWS_KEYPATH']}"

    aws.access_key_id = "#{ENV['AWS_ACCESS_KEY']}"
    aws.secret_access_key = "#{ENV['AWS_SECRET_KEY']}"
    aws.keypair_name = "#{ENV['AWS_KEYPAIR_NAME']}"
    aws.region = "us-west-2"
    aws.ami    = "ami-870a2fb7" # Ubuntu 14.04 LTS x64
    aws.instance_type = "t2.micro"
    aws.tags = {
      'instance' => 'bcube-restparql',
    }
  end

  config.vm.provision :fabric do |fabric|
    fabric.fabfile_path = "./fabfile.py"
    fabric.tasks = ["provision","run_app" ]
  end

  config.vm.network "forwarded_port", guest: 80, host: 8080

end