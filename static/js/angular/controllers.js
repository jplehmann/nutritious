'use strict';

/* Controllers */

angular.module('myApp.controllers', []).

    controller('BaseCtrl', ['$scope', '$http', '$window', '$timeout', 
            function ($scope, $http, $window, $timeout) {

      $scope.query = $.url().param('q');
      // reference and resource are initialized in html
      $scope.reference = undefined;
      $scope.resource = undefined;
      
      // Ctrl-S for copy
      $(document).bind('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.which === "S".charCodeAt(0)) {
          // go to search 
          $('#search-input').focus().select();
          e.preventDefault();
        }
      });

      // TEST:
      //$('#search_input').keypress(function(e) {
      //  console.log(e);
      //});
      //$('#search_input').val('#love');
      ////jQuery('#search_input').trigger(jQuery.Event('keypress', { which: 13 }));
      //$('#search_input').parent('form').submit();
    }]).
  
    controller('RefCtrl', ['$scope', '$http', '$window', 
            function ($scope, $http, $window) {

      //console.log(numsToRanges([1]));
      //console.log(numsToRanges([1,2]));
      //console.log(numsToRanges([1,3]));
      //console.log(numsToRanges([1,2,3]));
      //console.log(numsToRanges([1,3,4]));
      //console.log(numsToRanges([1,2,3,5,8,9,11,13,14]));

      function numsToRanges(nums) {
        //var sNums = sort(nums);
        var prev = -1;
        var prevWritten = -1;
        var ref = "";
        for (var i=0; i < nums.length; i++) {
          if (nums[i] == prev+1) {
            // do nothing if in a range
            prev = nums[i];
          } else {
            if (ref.length > 0) {
              if (prev !== prevWritten) {
                // if gapping and more than one in previous, bound it
                ref = ref + "-" + prev;
              }
              // close the last range
              ref = ref + ",";
            }
            // start the new range
            ref = ref + nums[i];
            prevWritten = nums[i];
            prev = nums[i];
          }
        }
        // close last open range
        if (prev !== -1 && prev !== prevWritten) {
          // if gapping and more than one in previous, bound it
          ref = ref + "-" + prev;
        }
        return ref;
      }

      $( "#selectable" ).selectable({
        filter: '.row-fluid',
        stop: function(event, ui) { 
          var selectedLines = [];
          var selectedText = "";
          // collect references
          angular.forEach($('#selectable .ui-selected a'), function(e) {
            // and why did .attr('x') not work on the whole list?
            // why is e not a jquery selector?
            //selectedLines.push($(e).attr('href'));
            selectedLines.push(parseInt($(e).text().trim()));
          });
          // collect text
          angular.forEach($('#selectable .ui-selected span'), function(e) {
            selectedText = selectedText.trim() + " " + $(e).text().trim();
          });
          $scope.selectedRef = $scope.reference + ":" + numsToRanges(selectedLines);
          $scope.selectedText = selectedText + "  (" + $scope.selectedRef + ")";
        }
      });

      // add the links back which selectable blew out
      $('.row-fluid a').click(function(e) {
        $window.location = e.target.href;
      });

      function copyToClipboard (text) {
        $window.prompt("Copy to clipboard: Ctrl+C, Enter", text);
      }

      // Ctrl-C for copy
      $(document).bind('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.which === "C".charCodeAt(0)) {
          copyToClipboard($scope.selectedText);
          e.preventDefault();
        }
      });
      
      // Ctrl-T for tag (Meta doesn't work)
      $(document).bind('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.which === "T".charCodeAt(0)) {
          // go to create tag URL
          // TODO: FIXME remove absolute
          $window.location = $scope.tagCreateUrl + "?res=" + $scope.resource +
            // if anything is selected, provide that ref/resource
            "&ref=" + ($scope.selectedRef || $scope.reference)
          e.preventDefault();
        }
      });
    }]).

    controller('TagCtrl', ['$scope', '$http', '$window', '$timeout', 
            function ($scope, $http, $window, $timeout) {

        $scope.resource = $.url().param('res');
        $scope.reference = $.url().param('ref');

        $scope.renameTag = function(tagName) {
            var newName = prompt("Enter new tag name");
            if (!newName) {
              return;
            }
            newName = newName.trim();
            // FIXME get link from server
            $http.put(tagName + "?name=" + newName)
                .success(function () {
                    console.log("rename successful");
                    $window.location.reload(true);
                }).error(function() {
                        console.log("rename failed");
                    });
                // TODO: redirect
        };

        $scope.deleteAllTags = function() {
            console.log("delete all called");
            // FIXME get link from server
            $http.delete()
                .success(function () {
                    console.log("delete successful");
                    $window.location.reload(true);
                }).error(function() {
                        console.log("delete failed");
                    });
                // TODO: redirect
        };

        $scope.deleteTag = function(tagName, id) {
            console.log("delete called: " + tagName);
            // FIXME get link from server
            $http.delete(tagName+ '/refs/'+ id)
                .success(function () {
                    console.log("delete successful");
                    $window.location.reload(true);
                }).error(function() {
                        console.log("delete failed");
                    });
                // TODO: redirect
        };

        $scope.deleteTagRef = function(id) {
            // FIXME get link from server
            var url = "refs/" + id;
            console.log("delete called: " + url);
            $http.delete(url)
                .success(function () {
                    console.log("delete successful");
                    $window.location.reload(true);
                }).error(function() {
                    console.log("delete failed");
                });
            // TODO: redirect
        };

        // focus on the first un-initialized field
        $timeout(function() {
          if (!$scope.tag) {
            $('#inputTag').focus();
          } else if (!$scope.resource) {
            $('#inputResource').focus();
          } else if (!$scope.reference) {
            $('#inputRef').focus();
          } else {
            $('#submitButton').focus();
          }
        });
    }]);
