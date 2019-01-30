widgetGenerators['note'] = {
	'variant': {
		'width': 280, 
		'height': 280, 
		'donterase': true,
        'variables': {'noterow': ''},
		'function': function (div, row, tabName) {
            var widgetName = 'note';
			var v = widgetGenerators[widgetName][tabName]['variables'];
            if (v['noterow'] == row[0]) {
                return;
            } else {
                $(div).empty();
            }
            v['noterow'] = row[0];
            var colNo = infomgr.getColumnNo(tabName, 'base__note');
            var note = row[colNo];
            var button = getEl('button');
            button.textContent = 'Save';
            button.addEventListener('click', function (evt) {
                var note = evt.target.nextSibling.nextSibling.value;
                $grids[tabName].pqGrid('getData')[selectedRowNos[tabName]][colNo] = note;
                $grids[tabName].pqGrid('refresh');
                $.ajax({
                    url: '/result/runwidget/note',
                    data: {'dbpath': dbPath, 
                           'tab': tabName, 
                           'rowkey': row[0],
                           'note': note,
                          },
                    success: function (response) {
                    }
                });
            });
            addEl(div, button);
            addEl(div, getEl('br'));
            var textbox = getEl('textarea');
            textbox.style.width = '100%';
            textbox.style.height = 'calc(100% - 24px)';
            textbox.value = note;
            addEl(div, textbox);
		}
	},
	'gene': {
		'width': 280,
		'height': 280,
		'donterase': true,
        'variables': {'noterow': ''},
		'function': function (div, row, tabName) {
            var widgetName = 'note';
			var v = widgetGenerators[widgetName][tabName]['variables'];
            if (v['noterow'] == row[0]) {
                return;
            } else {
                $(div).empty();
            }
            v['noterow'] = row[0];
            var colNo = infomgr.getColumnNo(tabName, 'base__note');
            var note = row[colNo];
            var button = getEl('button');
            button.textContent = 'Save';
            button.addEventListener('click', function (evt) {
                var note = evt.target.nextSibling.nextSibling.value;
                $grids[tabName].pqGrid('getData')[selectedRowNos[tabName]][colNo] = note;
                $grids[tabName].pqGrid('refresh');
                $.ajax({
                    url: '/result/runwidget/note',
                    data: {'dbpath': dbPath, 
                           'tab': tabName, 
                           'rowkey': row[0],
                           'note': note,
                          },
                    success: function (response) {
                    }
                });
            });
            addEl(div, button);
            addEl(div, getEl('br'));
            var textbox = getEl('textarea');
            textbox.style.width = '100%';
            textbox.style.height = 'calc(100% - 24px)';
            textbox.value = note;
            addEl(div, textbox);
		}
	}
}
