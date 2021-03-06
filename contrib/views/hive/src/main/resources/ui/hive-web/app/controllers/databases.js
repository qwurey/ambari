/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import Ember from 'ember';
import constants from 'hive/utils/constants';

export default Ember.Controller.extend({
  databaseService: Ember.inject.service(constants.namingConventions.database),
  notifyService: Ember.inject.service(constants.namingConventions.notify),

  pageCount: 10,

  selectedDatabase: Ember.computed.alias('databaseService.selectedDatabase'),
  databases: Ember.computed.alias('databaseService.databases'),

  tableSearchResults: Ember.Object.create(),

  tableControls: [
    {
      icon: 'fa-list',
      action: 'loadSampleData',
      tooltip: Ember.I18n.t('tooltips.loadSample')
    }
  ],

  panelIconActions: [
    {
      icon: 'fa-refresh',
      action: 'refreshDatabaseExplorer',
      tooltip: Ember.I18n.t('tooltips.refresh')
    }
  ],

  tabs: [
    Ember.Object.create({
      name: Ember.I18n.t('titles.explorer'),
      visible: true,
      view: constants.namingConventions.databaseTree
    }),
    Ember.Object.create({
      name: Ember.I18n.t('titles.results'),
      view: constants.namingConventions.databaseSearch
    })
  ],

  _handleError: function (error) {
    this.get('notifyService').error(error);
    this.set('isLoading', false);
  },

  setTablePageAvailability: function (database) {
    var result;

    if (database.get('hasNext')) {
      result = true;
    } else if (database.tables.length > database.get('visibleTables.length')) {
      //if there are hidden tables
      result = true;
    }

    database.set('canGetNextPage', result);
  },

  setColumnPageAvailability: function (table) {
    var result;

    if (table.get('hasNext')) {
      result = true;
    } else if (table.columns.length > table.get('visibleColumns.length')) {
      //if there are hidden columns
      result = true;
    }

    table.set('canGetNextPage', result);
  },

  selectedDatabaseChanged: function () {
    var self = this;

    this.set('isLoading', true);

    this.get('databaseService').getAllTables().then(function () {
      self.set('isLoading', false);
    }, function (err) {
      self._handleError(err);
    });
  }.observes('selectedDatabase'),

  getNextColumnPage: function (database, table) {
    var self = this;

    this.set('isLoading', true);

    if (!table.columns) {
      table.columns = [];
      table.set('visibleColumns', []);
    }

    this.get('databaseService').getColumnsPage(database.get('name'), table).then(function (result) {
      table.columns.pushObjects(result.columns);
      table.get('visibleColumns').pushObjects(result.columns);
      table.set('hasNext', result.hasNext);

      self.setColumnPageAvailability(table);
      self.set('isLoading', false);
    }, function (err) {
      self._handleError(err);
    });
  },

  getNextTablePage: function (database) {
    var self = this;

    this.set('isLoading', true);

    if (!database.tables) {
      database.tables = [];
      database.set('visibleTables', []);
    }

    this.get('databaseService').getTablesPage(database).then(function (result) {
      database.tables.pushObjects(result.tables);
      database.get('visibleTables').pushObjects(result.tables);
      database.set('hasNext', result.hasNext);

      self.setTablePageAvailability(database);
      self.set('isLoading', false);
    }, function (err) {
      self._handleError(err);
    });
  },

  getDatabases: function () {
    var self = this;
    var selectedDatabase = this.get('selectedDatabase');

    this.set('isLoading', true);

    this.get('databaseService').getDatabases().then(function (databases) {
      self.set('isLoading');
    }).catch(function (error) {
      self._handleError(error);

      if(error.status == 401) {
         self.send('passwordLDAPDB');
      }


    });
  }.on('init'),

  actions: {
    refreshDatabaseExplorer: function () {
      this.getDatabases();
    },

    passwordLDAPDB: function(){
      var self = this,
          defer = Ember.RSVP.defer();

      self.getDatabases = this.getDatabases;

      this.send('openModal', 'modal-save', {
        heading: "modals.authenticationLDAP.heading",
        text:"",
        type: "password",
        defer: defer
      });

      defer.promise.then(function (text) {
        // make a post call with the given ldap password.
        var password = text;
        var pathName = window.location.pathname;
        var pathNameArray = pathName.split("/");
        var hiveViewVersion = pathNameArray[3];
        var hiveViewName = pathNameArray[4];
        var ldapAuthURL = "/api/v1/views/HIVE/versions/"+ hiveViewVersion + "/instances/" + hiveViewName + "/jobs/auth";

        $.ajax({
          url: ldapAuthURL,
          dataType: "json",
          type: 'post',
          headers: {'X-Requested-With': 'XMLHttpRequest', 'X-Requested-By': 'ambari'},
          contentType: 'application/json',
          data: JSON.stringify({ "password" : password}),
          success: function( data, textStatus, jQxhr ){
            console.log( "LDAP done: " + data );
            self.getDatabases();
          },
          error: function( jqXhr, textStatus, errorThrown ){
            console.log( "LDAP fail: " + errorThrown );
            self.get('notifyService').error( "Wrong Credentials." );
          }
        });

      });
    },

    loadSampleData: function (tableName, database) {
      var self = this;
      this.send('addQuery', Ember.I18n.t('titles.tableSample', { tableName: tableName }));

      Ember.run.later(function () {
        var query = constants.sampleDataQuery.fmt(tableName);

        self.set('selectedDatabase', database);
        self.send('executeQuery', constants.jobReferrer.sample, query);
      });
    },

    getTables: function (dbName) {
      var database = this.get('databases').findBy('name', dbName),
          tables = database.tables,
          pageCount = this.get('pageCount');

      if (!tables) {
        this.getNextTablePage(database);
      } else {
        database.set('visibleTables', tables.slice(0, pageCount));
        this.setTablePageAvailability(database);
      }
    },

    getColumns: function (tableName, database) {
      var table = database.get('visibleTables').findBy('name', tableName),
          pageCount = this.get('pageCount'),
          columns = table.columns;

      if (!columns) {
        this.getNextColumnPage(database, table);
      } else {
        table.set('visibleColumns', columns.slice(0, pageCount));
        this.setColumnPageAvailability(table);
      }
    },

    showMoreTables: function (database) {
      var tables = database.tables,
          visibleTables = database.get('visibleTables'),
          visibleCount = visibleTables.length;

      if (!tables) {
        this.getNextTablePage(database);
      } else {
        if (tables.length > visibleCount) {
          visibleTables.pushObjects(tables.slice(visibleCount, visibleCount + this.get('pageCount')));
          this.setTablePageAvailability(database);
        } else {
          this.getNextTablePage(database);
        }
      }
    },

    showMoreColumns: function (table, database) {
      var columns = table.columns,
          visibleColumns = table.get('visibleColumns'),
          visibleCount = visibleColumns.length;

      if (!columns) {
        this.getNextColumnPage(database, table);
      } else {
        if (columns.length > visibleCount) {
          visibleColumns.pushObjects(columns.slice(visibleCount, visibleCount + this.get('pageCount')));
          this.setColumnPageAvailability(table);
        } else {
          this.getNextColumnPage(database, table);
        }
      }
    },

    searchTables: function (searchTerm) {
      var self = this,
          resultsTab = this.get('tabs').findBy('view', constants.namingConventions.databaseSearch),
          tableSearchResults = this.get('tableSearchResults');

      searchTerm = searchTerm ? searchTerm.toLowerCase() : '';

      this.set('tablesSearchTerm', searchTerm);
      resultsTab.set('visible', true);
      this.set('selectedTab', resultsTab);
      this.set('columnSearchTerm', '');
      this.set('isLoading', true);

      this.get('databaseService').getTablesPage(this.get('selectedDatabase'), searchTerm, true).then(function (result) {
        tableSearchResults.set('tables', result.tables);
        tableSearchResults.set('hasNext', result.hasNext);

        self.set('isLoading', false);
      }, function (err) {
        self._handleError(err);
      });
    },

    searchColumns: function (searchTerm) {
      var self = this,
          database = this.get('selectedDatabase'),
          resultsTab = this.get('tabs').findBy('view', constants.namingConventions.databaseSearch),
          tables = this.get('tableSearchResults.tables');

      searchTerm = searchTerm ? searchTerm.toLowerCase() : '';

      this.set('selectedTab', resultsTab);

      this.set('isLoading', true);

      tables.forEach(function (table) {
        self.get('databaseService').getColumnsPage(database.get('name'), table, searchTerm, true).then(function (result) {
          table.set('columns', result.columns);
          table.set('hasNext', result.hasNext);

          if (tables.indexOf(table) === tables.get('length') -1) {
            self.set('isLoading', false);
          }
        }, function (err) {
          self._handleError(err);
        });
      });
    },

    showMoreResultTables: function () {
      var self = this,
          database = this.get('selectedDatabase'),
          tableSearchResults = this.get('tableSearchResults'),
          searchTerm = this.get('tableSearchTerm');

      this.set('isLoading', true);

      this.get('databaseService').getTablesPage(database, searchTerm).then(function (tablesResult) {
        var tables = tableSearchResults.get('tables');
        var shouldGetColumns = tables.any(function (table) {
          return table.get('columns.length') > 0;
        });

        tables.pushObjects(tablesResult.tables);
        tableSearchResults.set('hasNext', tablesResult.hasNext);

        //if user has already searched for columns for the previously loaded tables,
        //load the columns search results for the newly loaded tables.
        if (shouldGetColumns) {
          tablesResult.tables.forEach(function (table) {
            self.get('databaseService').getColumnsPage(database.get('name'), table, self.get('columnSearchTerm'), true).then(function (result) {
              table.set('columns', result.columns);
              table.set('hasNext', result.hasNext);

              if (tablesResult.tables.indexOf(table) === tablesResult.tables.get('length') -1) {
                self.set('isLoading', false);
              }
            }, function (err) {
              self._handleError(err);
            });
          });
        } else {
          self.set('isLoading', false);
        }
      }, function (err) {
        self._handleError(err);
      });
    },

    showMoreResultColumns: function (table) {
      var self = this;

      this.set('isLoading', true);

      this.get('databaseService').getColumnsPage(this.get('selectedDatabase.name'), table, this.get('columnSearchTerm')).then(function (result) {
        table.get('columns').pushObjects(result.columns);
        table.set('hasNext', result.hasNext);

        self.set('isLoading', false);
      }, function (err) {
        self._handleError(err);
      });
    }
  }
});
