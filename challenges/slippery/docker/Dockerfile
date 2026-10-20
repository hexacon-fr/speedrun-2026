FROM php:8.2-apache

RUN apt-get update \
    && apt-get install -y --no-install-recommends libzip-dev \
    && docker-php-ext-install zip \
    && rm -rf /var/lib/apt/lists/*

# Listen on 1337 like the other challenges.
RUN sed -i 's/^Listen 80$/Listen 1337/' /etc/apache2/ports.conf \
    && sed -i 's/<VirtualHost \*:80>/<VirtualHost *:1337>/' /etc/apache2/sites-available/000-default.conf

COPY index.php /var/www/html/index.php

# The app is only ever supposed to write inside uploads/, so nothing here
# grants extra privilege on purpose -- it's a plain, realistic deployment
# where the app user owns its own webroot.
RUN mkdir -p /var/www/html/uploads \
    && chown -R www-data:www-data /var/www/html

COPY --chmod=444 flag.txt /flag

EXPOSE 1337
