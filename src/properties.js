/**
 * Title shown in browser tab and banner
 */
var title = 'Abstract Visual Reasoning – SurVis';

/** Relative directories */
var dataDir   = 'data/';
var jsDir     = 'js/';
var stylesDir = 'styles/';

/** Tag clouds (only keywords + authors for clarity) */
var tagCloudOptions = [
  { field: 'keywords', title: 'Keywords', minTagFrequency: 1 },
  { field: 'author',   title: 'Authors',  minTagFrequency: 1 }
];

/** Disable online editing for published site */
var editable = false;

/** Optional paper banner – deactivate */
var paper = null;

/** No extra pages for now */
var extraPages = {};

/** Custom style – leave blank or set your css path */
var customStyle = '';

/** Citation info – keep null */
var citations = null;
