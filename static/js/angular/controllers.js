'use strict';

/* Controllers */

angular.module('myApp.controllers', []).

    controller('BaseCtrl', ['$scope', '$http', function ($scope, $http) {

      $scope.params = $.url().param();

      $scope.query = $scope.params['q'];
      
      // Ctrl-S for copy
      $(document).bind('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.which === "S".charCodeAt(0)) {
          // go to search 
          $('#search_input').focus().select();
          e.preventDefault();
        }
      });

    }]).
  
    controller('RefCtrl', ['$scope', '$http', function ($scope, $http) {

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
          var refStr = $scope.reference + ":" + numsToRanges(selectedLines);
          var refAndText = selectedText + "  (" + refStr + ")"
          $scope.selectedText = refAndText;
        }
      });

      // add the links back which selectable blew out
      $('.row-fluid a').click(function(e) {
        window.location = e.target.href;
      });

      function copyToClipboard (text) {
        window.prompt("Copy to clipboard: Ctrl+C, Enter", text);
      }

      // Ctrl-C for copy
      $(document).bind('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.which === "C".charCodeAt(0)) {
          copyToClipboard($scope.selectedText);
        }
      });
    }]).

    controller('TagCtrl', ['$scope', '$http', function ($scope, $http) {

        $scope.renameTag = function(tagName) {
            var newName = prompt("Enter new tag name");
            if (!newName) {
              return;
            }
            newName = newName.trim();
            $http.put(tagName + "?name=" + newName)
                .success(function () {
                    console.log("rename successful");
                    window.location.reload(true);
                }).error(function() {
                        console.log("rename failed");
                    });
                // TODO: redirect
        };

        $scope.deleteTag = function(tagName) {
            console.log("delete called: " + tagName);
            $http.delete(tagName)
                .success(function () {
                    console.log("delete successful");
                    window.location.reload(true);
                }).error(function() {
                        console.log("delete failed");
                    });
                // TODO: redirect
        };

        $scope.deleteTagRef = function(id) {
            var url = "refs/" + id;
            console.log("delete called: " + url);
            $http.delete(url)
                .success(function () {
                    console.log("delete successful");
                    window.location.reload(true);
                }).error(function() {
                    console.log("delete failed");
                });
            // TODO: redirect
        };
    }]);
