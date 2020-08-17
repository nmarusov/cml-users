# Режим разработки

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# Развёртывание
```
git clone https://github.com/nmarusov/cml-users.git

cd cml-users/frontend

docker build -t cals/cml-users .

docker run -d -p 8081:8080 --rm --name cml-users-frontend cals/cml-users:latest
```