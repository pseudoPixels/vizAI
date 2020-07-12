<p align="center">
  <img src="https://github.com/pseudoPixels/vizAI/blob/master/graphaite/webapp/static/images/logoGraphaite.png" width="30%" title="Graph[ai]te">
</p>

## Graphaite

### 1.0 Installation

#### 1.1 Install Graphite requirements
```buildoutcfg
>>> git clone https://github.com/pseudoPixels/vizAI.git
>>> cd vizAI
>>> conda create -n vizAiEnv python=3.6
>>> conda activate vizAiEnv
>>> pip install -e .
```

#### 1.2 Install Couchdb API as its not available in pip

```
>>> git clone https://github.com/pseudoPixels/flask-couchdb.git
>>> cd flask-couchdb
>>> pip install .
```

#### 1.3 Install CouchDB

```
>>> curl -L https://couchdb.apache.org/repo/bintray-pubkey.asc | sudo apt-key add -
>>> echo "deb https://apache.bintray.com/couchdb-deb bionic main" | sudo tee -a /etc/apt/sources.list
>>> sudo apt update
>>> sudo apt install couchdb
```

Details of the CouchdDB installation command:: https://linuxize.com/post/how-to-install-couchdb-on-ubuntu-18-04/


Done!

### App Start
```buildoutcfg
>>> cd vizAI
>>> sh run.sh
```
