const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

axios.get('https://bukk.it/')
    .then((response) => {
        if(response.status === 200) {
            const html = response.data;
            const $ = cheerio.load(html);
            let bukkitList = [];
            $('td a').each(function(i, elem) {
                bukkitList[i] = {
                    title: $(this).text().trim(),
                    url: $(this).attr('href')
                }
            });
            const bukkitListTrimmed = bukkitList.filter(n => n != undefined )
            fs.writeFile('bukkitList.json',
                          JSON.stringify(bukkitListTrimmed, null, 4),
                          (err)=> console.log('File successfully written!'))
    }
}, (error) => console.log(err) );
