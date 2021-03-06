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

var App = require('app');

App.MainDashboardController = Em.Controller.extend({
  name: 'mainDashboardController',
  categorySelected: 'widgets',

  scRequest: function(request) {
    return App.router.get('mainServiceController').get(request);
  },

  isAllServicesInstalled: function() {
    return this.scRequest('isAllServicesInstalled');
  }.property('App.router.mainServiceController.content.content.@each',
    'App.router.mainServiceController.content.content.length'),

  isStartAllDisabled: function() {
    return this.scRequest('isStartAllDisabled');
  }.property('App.router.mainServiceController.isStartStopAllClicked',
    'App.router.mainServiceController.content.@each.healthStatus'),

  isStopAllDisabled: function() {
    return this.scRequest('isStopAllDisabled');
  }.property('App.router.mainServiceController.isStartStopAllClicked',
    'App.router.mainServiceController.content.@each.healthStatus'),

  gotoAddService: function() {
    App.router.get('mainServiceController').gotoAddService();
  },

  startAllService: function(event){
    App.router.get('mainServiceController').startAllService(event);
  },

  stopAllService: function(event){
    App.router.get('mainServiceController').stopAllService(event);
  },

  restartAllRequired: function(event){
    App.router.get('mainServiceController').restartAllRequired(event);
  }
});