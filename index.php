<?php

require __DIR__ . 'vendor/autoload.php';

use Rudolf\OAuth2\Client\Provider\Reddit;
use Symfony\Component\Dotenv\Dotenv;

$dotenv = new Dotenv();
$dotenv->load(__DIR__.'/.env');

$reddit = new Reddit([
    'clientId'      => 'yourClientId',
    'clientSecret'  => 'yourClientSecret',
    'redirectUri'   => 'yourRedirectUri',
    'userAgent'     => 'platform:appid:version, (by /u/username)',
    'scopes'        => ['identity', 'read'],
]);