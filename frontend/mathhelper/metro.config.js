const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Supabase ships .mjs files that Metro doesn't resolve by default
config.resolver.sourceExts.push('mjs');

module.exports = config;
