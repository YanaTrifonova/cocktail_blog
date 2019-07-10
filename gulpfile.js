const gulp = require('gulp');
const sass = require('gulp-sass');
const autoprefixer = require('gulp-autoprefixer');

function css() {
    return gulp
        .src('scss/main.scss')
        .pipe(sass({outputStyle: 'expanded'}).on('error', sass.logError))
        .pipe(autoprefixer({
            browsers: ['last 2 versions']
        }))
      //  .pipe(gulp.dest('static/stylesheet'))
        .pipe(sass.sync({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(gulp.dest('static/stylesheet'))
}

function watchFiles() {
    gulp.watch('scss/**', css);
    gulp.watch('templates/index.html')
}

gulp.task('css', css);
gulp.task('watch', gulp.parallel(watchFiles));
