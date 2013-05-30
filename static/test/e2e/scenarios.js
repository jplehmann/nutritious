'use strict';
 
/* http://docs.angularjs.org/guide/dev_guide.e2e-testing */

// TODO: create testing account, and "delete all tags" option.
//
// When testing use this account and clear all the import fixture.
// 
// TODO: add link within tagz to run all tests.

describe('Nutritious home', function() {

  beforeEach(function() {
    browser().navigateTo('../../..');
  });

  it('should be home at the root', function() {
    expect(element('title').text()).toContain('Tagz - Home');
  });

  it('library should contain NASB', function() {
    element('#lib-link').click();
    expect(element('.content a').text()).toContain('NASB');
    element('#res-NASB').click();
    expect(element('.content h2').text()).toContain('NASB');
  });
});

describe('Nutritious search', function() {

  beforeEach(function() {
    browser().navigateTo('../../..');
  });

  it('with Keywords should find hits', function() {
    search('Adam', 'NASB');
    expect(element('.content h2').text()).toContain("Search of 'NASB' for 'Adam' (21 hits)");
    expect(element('.row-fluid span').text())
        .toContain("It was also about these men that Enoch");
  });

  it('with Reference should find a Line', function() {
    search('jn 3:16', 'NASB');
    expect(element('.content div').text())
        .toContain("For God so loved the world,");
  });
  
  it('with Reference should find a Chapter', function() {
    search('jn 3', 'NASB');
    expect(element('.content div').text())
        .toContain("Now there was a man of the Pharisees");
    expect(element('.content div').text())
        .toContain("He who believes in the Son has eternal life");
  });
  
  it('with Reference should find a Book', function() {
    search('jn', 'NASB');
    expect(element('.content a').text()).toContain("John 1");
    expect(element('.content a').text()).toContain("John 21");
  });

  it('with Tag should find hits', function() {
    search('#love');
    expect(element('a').text()).toContain('John 3:16');
    expect(element('a').text()).toContain('Romans 5:8');
    expect(element('a').text()).toContain('1 John 4:19');
  });
  
});

xdescribe('Run one test', function() {
  beforeEach(function() {
    browser().navigateTo('../../..');
  });

});


// 
// Utility functions
//
function search(query, resource) {
  if (resource) {
    browser().navigateTo('../../../lib/' + resource);
  }
  inputElement('#search_input').enter(query);
  element("#search-submit").click();
  sleep(0.3);
}




/*
describe('PhoneCat App', function() {

  it('should redirect index.html to index.html#/phones', function() {
    browser().navigateTo('../../app/index.html');
    expect(browser().location().url()).toBe('/phones');
  });


  describe('Phone list view', function() {

    beforeEach(function() {
      browser().navigateTo('../../app/index.html#/phones');
    });


    it('should filter the phone list as user types into the search box', function() {
      expect(repeater('.phones li').count()).toBe(20);

      input('query').enter('nexus');
      expect(repeater('.phones li').count()).toBe(1);

      input('query').enter('motorola');
      expect(repeater('.phones li').count()).toBe(8);
    });


    it('should be possible to control phone order via the drop down select box', function() {
      input('query').enter('tablet'); //let's narrow the dataset to make the test assertions shorter

      expect(repeater('.phones li', 'Phone List').column('phone.name')).
          toEqual(["Motorola XOOM\u2122 with Wi-Fi",
                   "MOTOROLA XOOM\u2122"]);

      select('orderProp').option('Alphabetical');

      expect(repeater('.phones li', 'Phone List').column('phone.name')).
          toEqual(["MOTOROLA XOOM\u2122",
                   "Motorola XOOM\u2122 with Wi-Fi"]);
    });


    it('should render phone specific links', function() {
      input('query').enter('nexus');
      element('.phones li a').click();
      expect(browser().location().url()).toBe('/phones/nexus-s');
    });
  });


  describe('Phone detail view', function() {

    beforeEach(function() {
      browser().navigateTo('../../app/index.html#/phones/nexus-s');
    });


    it('should display nexus-s page', function() {
      expect(binding('phone.name')).toBe('Nexus S');
    });


    it('should display the first phone image as the main phone image', function() {
      expect(element('img.phone').attr('src')).toBe('img/phones/nexus-s.0.jpg');
    });


    it('should swap main image if a thumbnail image is clicked on', function() {
      element('.phone-thumbs li:nth-child(3) img').click();
      expect(element('img.phone').attr('src')).toBe('img/phones/nexus-s.2.jpg');

      element('.phone-thumbs li:nth-child(1) img').click();
      expect(element('img.phone').attr('src')).toBe('img/phones/nexus-s.0.jpg');
    });
  });
*/

// Example of how to get access to jQuery
//angular.scenario.dsl('appElement', function() {
//  return function(selector, fn) {
//    return this.addFutureAction('element ' + selector, function($window, $document, done) {
//      var $ = $window.$; 
//      // pass the jquery element as well as jquery back
//      fn.call(this, $window.angular.element(selector), $);
//      done();
//    });
//  };
//});

