widgetGenerators['dbsnp'] = {
	'variant': {
		'width': 280, 
		'height': 80, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'dbSNP', 'dbsnp__snp', tabName);
		}
	}
}
