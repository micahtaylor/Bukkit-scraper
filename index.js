const express = require('express');
const app = express();
// const loadJsonFile = require('load-json-file');

app.set('views', './views')
app.set('view engine', 'ejs')
app.get('/', function (req, res) {
  app.render('index');

  // loadJsonFile('bukkitList.json').then(json => {
      // console.log(json);
      //=> {foo: true}
  // });
})
app.listen(3000, () => console.log('Example app listening on port 3000!'))
