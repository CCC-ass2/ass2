module.exports = function (grunt) {
  grunt
    .initConfig({
      "couch-compile": {
        dbs: {
          files: {
            "/tmp/au_covid.json": "couchdb/twitter/covid",
            "/tmp/au_employment.json": "couchdb/twitter/employment",
            "/tmp/au_main.json": "couchdb/twitter/stress"
          }
        }
      },
      "couch-push": {
        options: {
          user: process.env.user,
          pass: process.env.pass
        },
        twitter: {

        }
      }
    });

  grunt.config.set(`couch-push.twitter.files.http://admin:admin@172\\.26\\.133\\.30:5984/${process.env.dbname1}`, "/tmp/au_covid.json");
  // grunt.config.set(`couch-push.twitter.files.http://admin:admin@172\\.26\\.133\\.30:5984/${process.env.dbname2}`, "/tmp/au_employment.json");
  grunt.config.set(`couch-push.twitter.files.http://admin:admin@172\\.26\\.133\\.30:5984/${process.env.dbname3}`, "/tmp/au_main.json");

console.log(JSON.stringify(grunt.config.get()));
  grunt.loadNpmTasks("grunt-couch");
};
