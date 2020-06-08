'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var minifyCSS = require('gulp-clean-css');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var changed = require('gulp-changed');
var watch = require('gulp-watch');

var SCSS_SRC = './src/Assets/scss/**/*.scss';
var SCSS_DEST = './src/Assets/css';

function compile_scss(){
gulp.src(SCSS_SRC)
.pipe(sass().on('error',sass.logError))
.pipe(minifyCSS())
.pipe(rename({suffix: '.min'}))
.pipe(changed(SCSS_DEST))
.pipe(gulp.dest(SCSS_DEST));
}

function watch_css(SCSS_SRC){
  watch(SCSS_SRC, compile_scss());
}

function defaultTask(){
  watch_css();
}

exports.default=defaultTask;