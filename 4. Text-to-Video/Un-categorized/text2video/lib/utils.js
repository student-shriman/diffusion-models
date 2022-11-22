/*
 * Copyright 2014, Gregg Tavares.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 *     * Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above
 * copyright notice, this list of conditions and the following disclaimer
 * in the documentation and/or other materials provided with the
 * distribution.
 *     * Neither the name of Gregg Tavares. nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
"use strict";

var debug   = require('debug')('utils');
var fs      = require('fs');
var path    = require('path');
var tmp     = require('tmp');

tmp.setGracefulCleanup();

var execute = function(cmd, args, callback) {
  var spawn = require('child_process').spawn;

  var proc = spawn(cmd, args);
  var stdout = [];
  var stderr = [];

  proc.stdout.setEncoding('utf8');
  proc.stdout.on('data', function (data) {
      var str = data.toString()
      var lines = str.split(/(\r?\n)/g);
      stdout = stdout.concat(lines);
  });

  proc.stderr.setEncoding('utf8');
  proc.stderr.on('data', function (data) {
      var str = data.toString()
      var lines = str.split(/(\r?\n)/g);
      stderr = stderr.concat(lines);
  });

  proc.on('close', function (code) {
    var code = parseInt(code);
    var result = {
      code: code,
      fuck: "fuckyou",
      stdout: stdout.join(""),
      stderr: stderr.join(""),
    };
    if (code !== 0) {
      callback(result);
    } else {
      callback(null, result)
    }
  });
}

var getTempFilename = function(options) {
  options = options || {};
  return new Promise(function(fulfill, reject) {
    tmp.tmpName(options, function(err, filePath) {
      if (err) {
        reject(err);
      } else {
        fulfill(filePath);
      }
    });
  });
};

var getTempFolder = function(options) {
  options = options || {};
  return new Promise(function(fulfill, reject) {
    tmp.dir(options, function(err, filePath) {
      if (err) {
        reject(err);
      } else {
        fulfill(filePath);
      }
    });
  });
};

var deleteNoFail = function(filePath) {
  if (filePath && fs.existsSync(filePath)) {
    if (fs.lstatSync(filePath).isDirectory()) {
      fs.rmdirSync(filePath);
    } else {
      fs.unlinkSync(filePath);
    }
  }
};

var copyFile = function(src, dst, options) {
  options = options || {};
  var fs = options.fileSystem || require('fs');
  var data = fs.readFileSync(src);
  fs.writeFileSync(dst, data);
  var srcStat = fs.statSync(src);
  var execBits = (1 << 0) | (1 << 3) | (1 << 6);
  var srcExecBits = srcStat.mode & execBits;
  if (srcExecBits) {
    var dstStat = fs.statSync(dst);
    fs.chmodSync(dst, dstStat.mode | srcExecBits)
  }
};

exports.copyFile = copyFile;
exports.deleteNoFail = deleteNoFail;
exports.getTempFolder = getTempFolder;
exports.getTempFilename = getTempFilename;
exports.execute = execute;

