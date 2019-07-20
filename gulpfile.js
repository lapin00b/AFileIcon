"use strict";

/*
 * Plugins
 */

var gulp = require("gulp");
var color = require("color");
var colors = require("colors");
var path = require("path");
var argv = require("yargs").argv;
var fs = require("fs");
var merge = require("merge-stream");
var $ = require("gulp-load-plugins")();

/*
 * Options
 */

var opts = {};

opts.colors = require("./common/colors.json");
opts.sizes = require("./common/sizes.json");

/*
 * Helpers
 */

var getIconOpts = function() {
  return JSON.parse(fs.readFileSync("./common/icons.json", "utf8"));
};

var getIconScope = function(iconOpts) {
  var syntaxes = iconOpts.syntaxes;
  var aliases = iconOpts.aliases;

  var scope = "";

  if (syntaxes) {
    for (var syntax in syntaxes) {
      scope = scope + syntaxes[syntax].scope + ", ";
    }
  }

  if (aliases) {
    for (var alias in aliases) {
      scope = scope + aliases[alias].scope + ", ";
    }
  }

  return scope.slice(0, -2);
};

/*
 * Build
 */

// Icons

gulp.task("build:icons", function() {
  var baseColor = $.recolorSvg.ColorMatcher(color("#000"));

  opts.icons = getIconOpts();

  return gulp.src("./common/assets/*.svg")
    .pipe($.plumber(function(error) {
      console.log("[build:icons]".bold.magenta + " There was an issue rasterizing icons:\n".bold.red + error.message);
      this.emit("end");
    }))
    .pipe($.changed("./icons/multi", {extension: ".png"}))
    .pipe($.flatmap(function(stream, file) {
      var iconName = path.basename(file.path, path.extname(file.path));
      var iconOpts = opts.icons[iconName];
      var iconColor = color(opts.colors[iconOpts.color]);

      var iconImages = merge();

      iconImages.add(opts.sizes.map(function(size) {
        var multi = gulp.src(file.path)
          .pipe($.recolorSvg.Replace(
            [baseColor],
            [iconColor]
          ))
          .pipe($.svg2png({
            width: size.size,
            height: size.size
          }))
          .pipe($.if(size.size, $.rename({suffix: size.suffix})))
          .pipe($.imagemin([$.imagemin.optipng({
            bitDepthReduction: false,
            colorTypeReduction: false,
            paletteReduction: false
          })], {verbose: true}))
          .pipe(gulp.dest("./icons/multi"));

        var single = gulp.src(file.path)
          .pipe($.recolorSvg.Replace(
            [baseColor],
            [color("white")]
          ))
          .pipe($.svg2png({
            width: size.size,
            height: size.size
          }))
          .pipe($.if(size.size, $.rename({suffix: size.suffix})))
          .pipe($.imagemin([$.imagemin.optipng({
            bitDepthReduction: false,
            colorTypeReduction: false,
            paletteReduction: false
          })], {verbose: true}))
          .pipe(gulp.dest("./icons/single"));

        return merge(multi, single);
      }));

      return iconImages;
    }));
});

/*
 * Release
 */

gulp.task("media", function() {
  return gulp.src("./media/*.{png,jpg}")
    .pipe($.imagemin({verbose: true}))
    .pipe(gulp.dest("./media"));
});


gulp.task("bump-version", function() {
  return gulp.src("./package.json")
    .pipe($.if(argv.patch, $.bump({ type: "patch" })))
    .pipe($.if(argv.minor, $.bump({ type: "minor" })))
    .pipe($.if(argv.major, $.bump({ type: "major" })))
    .pipe(gulp.dest("./"));
});
