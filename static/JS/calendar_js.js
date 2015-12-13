/**
 * Created by ryan on 15/12/9.
 */
function getMonthJuZhen(date){    //argument[0]包含了日期的全部信息
	if(arguments.length == 0){
		throw new Error("need a date");
	}
	if(arguments[0] == null){
		throw new Error("date is null or undefined");
	}
	if(arguments[0] instanceof Date){   //arguments[0]是Date的实例
		var monthjuzhen = new Array(5);
		for(var r = 0 ; r < 5 ; r++){
			monthjuzhen[r] = [0,0,0,0,0,0,0];   //5*7的月份矩阵
		}
		var maxDay = getMaxDay(arguments[0]);   //调用getMaxDay 获取该月的天数
		arguments[0].setDate(1);    //设置成一月
		var r = 0;    //月份矩阵的横行
		var c = arguments[0].getDay();   //周几
		for(var d = 1 ; d <= maxDay ; d++){
			monthjuzhen[r][c] = d;
			if(c == 6){
				if(r == 4){
					r = 0;    //这个机制让31号显示在了1号同一行
				}
				else{
					r++;
				}
				c = 0;
			}
			else{
				c++;
			}
		}
		return monthjuzhen;
	}
	else{
		throw new Error("need a date");
	}
}


//getMaxDay()
function getMaxDay(date){
	if(arguments.length == 0){
		throw new Error("need a date");
	}
	if(arguments[0] == null){
		throw new Error("date is null or undefined");
	}
	if(arguments[0] instanceof Date){
		var tempDate = new Date(arguments[0].toString());
		if(arguments[0].getMonth() == 11){   //表明是12月   tempDate变为次年一月
			tempDate.setFullYear((tempDate.getFullYear()+1));
			tempDate.setMonth(0);
		}
		else{
			tempDate.setMonth((tempDate.getMonth()+1));    //tempDate月份加一
		}
		return Math.floor((tempDate.getTime()-arguments[0].getTime())/(1000*60*60*24));  //后面1000*60*60*24是1天的毫秒数  getTime()函数计算从1970年1月1日到现在的毫秒数
	}
	else{
		throw new Error("need a date");
	}
}

//updateDate
function updateDate(aa){
	var yearInput = document.getElementById("yearinput");
	var monthInput = document.getElementById("monthinput");
	try{
		var year = parseInt(yearInput.value);   //获取输入的年份
		var month = parseInt(monthInput.value); //获取输入的月份
		if(isNaN(year)){    //年份、月份输入非数字,将其值变为“”
			if(isNaN(month)){
				monthInput.value = "";
			}
		yearInput.value = "";
		return;
		}
		if(isNaN(month)){
			monthInput.value = "";
			return;
		}
		if(month > 12 || month < 1){   //检测月份输入是否合法
			monthInput.value = "";
			return;
		}
		month--;
		var date = new Date(year,month);   //根据创建了一个日期对象
		var monthjuzhen = getMonthJuZhen(date);    //获取所输月份的矩阵
		var day;
		var dayvalue;
		for(var r in monthjuzhen){   //r是一维数组 是月份矩阵的某一行
			for(var c in monthjuzhen[parseInt(r)]){
				day = document.getElementById(r+"-"+c);   //表示一个td
				dayvalue = monthjuzhen[parseInt(r)][parseInt(c)];    //获取第r行、第c列的值
				if(dayvalue == 0){
					if(day.hasChildNodes()){
						day.removeChild(day.firstChild);
					}
					day.onmouseover = null;
					day.onmouseout = null;
					day.onclick = null;
					continue;
				}
				var date1 = day.getElementsByTagName('div')[0]
				//alert(date1);
				//alert(dayvalue);

				date1.innerHTML = dayvalue;


				//if(day.hasChildNodes()){    //判断该格子是否有子节点，有说明有内容
				//	day.firstChild.nodeValue = dayvalue;   //故只需更改子节点内容
				//}
				//else{
				//	day.appendChild(document.createTextNode(dayvalue));    //否则添加一个文本子节点，内容显示为该格子的日期
				//}
				//day.setAttribute("date",year+"-"+month+"-"+dayvalue);
				//day.onclick = subDate;
			}
		}
	}
	catch(e){
		alert(e);
	}
}

//subDate()
function subDate(){
    var date = this.getAttribute("date").match(/(\d+)-(\d+)-(\d+)/);
    alert(new Date(date[1],date[2],date[3]));
}