
// The following javascript is to be used in UDF function to normalize names from bigquery
// the name normalizations are taken from this google doc: 
// https://docs.google.com/spreadsheets/d/1DZ_7VAbGS63wSRk8Yac00O0oTqgdFu66OnB_oFcvxOg/edit#gid=1459190414
// We haven't yet worked on the non-roman characters



// convert to roman numerals. If it is not a roman numeral, return 'false'


function deromanize(str) {
	var	str = str.toUpperCase(),
		validator = /^M*(?:D?C{0,3}|C[MD])(?:L?X{0,3}|X[CL])(?:V?I{0,3}|I[XV])$/,
		token = /[MDLV]|C[MD]?|X[CL]?|I[XV]?/g,
		key = {M:1000,CM:900,D:500,CD:400,C:100,XC:90,L:50,XL:40,X:10,IX:9,V:5,IV:4,I:1},
		num = 0, m;
	if (!(str && validator.test(str)))
		return false;
	while (m = token.exec(str))
		num += key[m[0]];
	return num;
};


function normalizeName(vessel){ 

  //Get rid of roman numerals
	vs = vessel.split(" ");
	rom = deromanize(vs[vs.length-1]);
	if(rom){
	    vs[vs.length-1] = rom;
	    vessel = vs.join(' ');
	}
	// if the vessel is vessel 036, change to vessel 36
	if(!isNaN(vs[vs.length-1])){
		vs[vs.length-1] = parseInt(vs[vs.length-1]);
	    vessel = vs.join(' ');
	}
  
  vessel = vessel.replace(/\s/g,''); // get rid of white spaces
  
	// If the vessel is 'ORYONG NO.715' change it to ORYONG 715
	// Similarly, 'NO.715 ORYONG' should also be ORYONG 715
	var number_find = /no\.[0-9]*/gi;
	no_array = 	vessel.match(number_find)||[];
    // We are only going to normalize the names of vessels that have "no." one time
	if (no_array.length == 1){
		vessel = vessel.replace(number_find,"")+no_array[0].replace(/no\./i,"");
	}	

	vessel = vessel.replace(/\./g,""); // get rid of periods
	vessel = vessel.replace(/\'/g,""); // get rid of single quotes
	vessel = vessel.replace(/f\/b/ig,''); // get rid of all F/B
	vessel = vessel.replace(/f\/v/ig,''); // get rid of 
	vessel = vessel.replace(/#/g,''); // get ride of #
	vessel = vessel.replace(/-/g,''); // get ride of -
	return vessel.toUpperCase(); // make uppercase and return

}



// The following is to test this code

// Example normalizations and the example outputs
vessels = ["ORYONG NO.715","AURORA B.","LUQINGYUANYU 026","NO.355 OYANG","XINSHIJI73HAO",".GREEN TUNA-1","CAPT.VINCENT GANN","KOO'S 102","311ORYONG","OCEAN WILD II","GOLFE DU LION V","GOLFE DU LYON VI","BAIAJI NO.3 / HAI HSIANG NO.81","AGUNG MAKMUR XXVII","BINTANG BATAVIA - I","VESSEL 1/1189","IMULA0012CHW","COSTA DE SÃO JORGE","HEMISFÉRIO NORTE","DONG BANN CHYOU NO.28Â ","Passarinho","Xin Shi Ji Nº 67","ITSWOSPOR037","F/B DANIEL DAVE VII","F/B EL NIÃ‘O","F/V GABRIELLE L.T.","F/B 808","DoÃ±a Blanca I","NIÃ‘A ZAIRA","Chia Yu #3","Albacora Catorce","KOTOSHIRO MARUã€€No. 8","Ã‡INAR BALIKÃ‡ILIK","KIYAK KARDEÅžLER-3","GEÃ‡Ä°CÄ°LER-4"];
desired_vessel_names = ["ORYONG715","AURORAB","LUQUINGYUANYU26","OYANG355","XINSHIJI73","GREENTUNA1","CAPTVINCENTGANN","KOOS102","ORYONG311","OCEANWILD2","GOLFEDULION5","GOLFEDULYON6","BAIAJI3","AGUNGMAKMUR27","BINTANGBATAVIA1","","","COSTADESAOJORGE","HEMISFERIONORTE","DONGBANNCHYOU28","PASSARINHO","XINSHIJI67","","DANIELDAVE8","ELNINO","GABRIELLELT","808","DONABLANCA1","NINAZAIRA","CHIAYU3","ALBACORA14","KOTOSHIROMARU8","CINARBALIKCILIK","KIYAKKARDESLER3","GECICILER4"];
desired_display_names = ["ORYONG 715","AURORA B","LUQINGYUANYU 26","OYANG 355","XINSHIJI 73","GREEN TUNA 1","CAPT VINCENT GANN","KOOS 102","ORYONG 311","OCEAN WILD 2","GOLFE DU LION 5","GOLFE DU LYON 6","BAIAJI 3","AGUNG MAKMUR 27","BINTANG BATAVIA 1","","","COSTA DE SAO JORGE","HEMISFERIO NORTE","DONG BANN CHYOU 28","PASSARINHO","XIN SHI JI 67","","DANIEL DAVE 8","EL NINO","GABRIELLE L T","808","DONA BLANCA 1","NINA ZAIRA","CHIA YU 3","ALBACORA 14","KOTOSHIRO MARU 8","CINAR BALIKCILIK","KIYAK KARDESLER 3","GECICILER 4"];

for(var i = 0; i<vessels.length;i++){
	console.log(vessels[i]+"\t"+normalizeName(vessels[i]));
}



// The following is to normalize a table with type 5 and 24 identifiers:


function normalize5_24Name(row, emit) {
  var shipname = row.shipname;
  if(shipname){
    shipname =  normalizeName(shipname);
  }
  
  emit({
    type:row.type,
    mmsi:row.mmsi,
    shipname:shipname,
    shiptype_text:row.shiptype_text,
    callsign:row.callsign,
    timestamp:row.timestamp,
    lon:row.lon,
    lat:row.lat,
    speed:row.speed,
    course:row.course,
    tagblock_station:row.tagblock_station 
  });
}



bigquery.defineFunction(
  'normalize5_24Name',  // Name of the function exported to SQL
  
  ['type','mmsi','shipname',
   'shiptype_text','callsign',
   'timestamp','lon','lat','speed',
   'course','tagblock_station'],  // Names of input columns
  
  [{'name':'type','type':'integer'},
  {'name':'mmsi','type':'integer'},
  {'name':'imo','type':'integer'},
  {'name':'shipname','type':'string'},
  {'name':'shiptype_text','type':'string'},
  {'name':'callsign','type':'string'},
  {'name':'timestamp','type':'timestamp'},
  {'name':'lon','type':'float'},
  {'name':'lat','type':'float'},
  {'name':'speed','type':'float'},
  {'name':'course','type':'float'},
  {'name':'tagblock_station','type':'string'}],
  
  normalize5_24Name                       // Reference to JavaScript UDF
);




////// now for [Registry_matching_sources.CLAV_cons_imo2]
/// saved output to [Registry_matching_sources.CLAV_cons_imo2_NORM]


function normalizeClav_cons_imo2(row, emit) {
  var new_shipname =  row.shipname;
  
  if(new_shipname){
    new_shipname = normalizeName(new_shipname);
  }

  emit({
	shiptype:row.shiptype,
	valid_from:row.valid_from,
	valid_to:row.valid_to,
	shipname:row.shipname,
	geartype:row.geartype,
	flag:row.flag,
	callsign:row.callsign,
	imo:row.imo,
	tonnage:row.tonnage,
	length:row.length,
	national_id:row.national_id,
	rfmo_id:row.rfmo_id,
	rfmo_name:row.rfmo_name,
	notes:row.notes,
	clav_VRMFID:row.clav_VRMFID,
	clav_DateUpdated:row.clav_DateUpdated,
	clav_TUVI:row.clav_TUVI,
	clav_FlagCode:row.clav_FlagCode,
	clav_ParentVesselTypeCode:row.clav_ParentVesselTypeCode,
	clav_ParentVesselType:row.clav_ParentVesselType,
	clav_VesselTypeCode:row.clav_VesselTypeCode,
	clav_GearTypeCode:row.clav_GearTypeCode,
	clav_LengthTypeCode:row.clav_LengthTypeCode,
	clav_TonnageTypeCode:row.clav_TonnageTypeCode,
	clav_PreviousName:row.clav_PreviousName,
	clav_PreviousNameDate:row.clav_PreviousNameDate,
	clav_PreviousFlagCode:row.clav_PreviousFlagCode,
	clav_PreviousFlagCodeDate:row.clav_PreviousFlagCodeDate,
	clav_AutStatus:row.clav_AutStatus,
	clav_DateAutStart:row.clav_DateAutStart,
	clav_DateAutEnd:row.clav_DateAutEnd,
	clav_DateAutTerm:row.clav_DateAutTerm,
	clav_AutTermCode:row.clav_AutTermCode,
	clav_AutTermDescription:row.clav_AutTermDescription,
	clav_AutTermReason:row.clav_AutTermReason,
	clav_URLID:row.clav_URLID,
	calc_normshipname:new_shipname,
	issf_imo_valid_from:row.issf_imo_valid_from,
	issf_imo_valid_to:row.issf_imo_valid_to,
	issf_imo_shipname:row.issf_imo_shipname,
	issf_imo_flag:row.issf_imo_flag,
	issf_imo_imo:row.issf_imo_imo,
	issf_imo_issf_Vessel_Type:row.issf_imo_issf_Vessel_Type,
	cons_imo:row.cons_imo,
	cnt_imo:row.cnt_imo,
	cons_imo2:row.cons_imo2  });
}



bigquery.defineFunction(
  'normalizeClav_cons_imo2',  // Name of the function exported to SQL
  
  ['shiptype','valid_from','valid_to','shipname','geartype','flag','callsign','imo','tonnage',
'length','national_id','rfmo_id','rfmo_name','notes','clav_VRMFID','clav_DateUpdated','clav_TUVI',
'clav_FlagCode','clav_ParentVesselTypeCode','clav_ParentVesselType','clav_VesselTypeCode',
'clav_GearTypeCode','clav_LengthTypeCode','clav_TonnageTypeCode','clav_PreviousName',
'clav_PreviousNameDate','clav_PreviousFlagCode','clav_PreviousFlagCodeDate','clav_AutStatus',
'clav_DateAutStart','clav_DateAutEnd','clav_DateAutTerm','clav_AutTermCode',
'clav_AutTermDescription','clav_AutTermReason','clav_URLID','calc_normshipname','issf_imo_valid_from',
'issf_imo_valid_to','issf_imo_shipname','issf_imo_flag','issf_imo_imo','issf_imo_issf_Vessel_Type',
'cons_imo','cnt_imo','cons_imo2'],  // Names of input columns
  
  [{'name':'shiptype','type':'string'},
	{'name':'valid_from','type':'timestamp'},
	{'name':'valid_to','type':'timestamp'},
	{'name':'shipname','type':'string'},
	{'name':'geartype','type':'string'},
	{'name':'flag','type':'string'},
	{'name':'callsign','type':'string'},
	{'name':'imo','type':'string'},
	{'name':'tonnage','type':'float'},
	{'name':'length','type':'float'},
	{'name':'national_id','type':'string'},
	{'name':'rfmo_id','type':'string'},
	{'name':'rfmo_name','type':'string'},
	{'name':'notes','type':'string'},
	{'name':'clav_VRMFID','type':'string'},
	{'name':'clav_DateUpdated','type':'timestamp'},
	{'name':'clav_TUVI','type':'string'},
	{'name':'clav_FlagCode','type':'string'},
	{'name':'clav_ParentVesselTypeCode','type':'string'},
	{'name':'clav_ParentVesselType','type':'string'},
	{'name':'clav_VesselTypeCode','type':'string'},
	{'name':'clav_GearTypeCode','type':'string'},
	{'name':'clav_LengthTypeCode','type':'string'},
	{'name':'clav_TonnageTypeCode','type':'string'},
	{'name':'clav_PreviousName','type':'string'},
	{'name':'clav_PreviousNameDate','type':'timestamp'},
	{'name':'clav_PreviousFlagCode','type':'string'},
	{'name':'clav_PreviousFlagCodeDate','type':'timestamp'},
	{'name':'clav_AutStatus','type':'string'},
	{'name':'clav_DateAutStart','type':'timestamp'},
	{'name':'clav_DateAutEnd','type':'timestamp'},
	{'name':'clav_DateAutTerm','type':'timestamp'},
	{'name':'clav_AutTermCode','type':'string'},
	{'name':'clav_AutTermDescription','type':'string'},
	{'name':'clav_AutTermReason','type':'string'},
	{'name':'clav_URLID','type':'string'},
	{'name':'calc_normshipname','type':'string'},
	{'name':'issf_imo_valid_from','type':'timestamp'},
	{'name':'issf_imo_valid_to','type':'timestamp'},
	{'name':'issf_imo_shipname','type':'string'},
	{'name':'issf_imo_flag','type':'string'},
	{'name':'issf_imo_imo','type':'integer'},
	{'name':'issf_imo_issf_Vessel_Type','type':'string'},
	{'name':'cons_imo','type':'integer'},
	{'name':'cnt_imo','type':'integer'},
	{'name':'cons_imo2','type':'integer'}],
  
  normalizeClav_cons_imo2                       // Reference to JavaScript UDF
);


///// Normalize EU query


function normalize_EU(row, emit) {
  var shipname_norm = row.shipname;
  if(shipname_norm){
    shipname_norm =  normalizeName(shipname_norm);
  }
  
  emit({
    row_number:row.row_number,
    Country_Code:row.Country_Code,
    CFR:row.CFR,
    Event_Code:row.Event_Code,
    Event_Start_Date:row.Event_Start_Date,
    Event_End__ate:row.Event_End__ate,
    License_Ind:row.License_Ind,
    Registration_Nbr:row.Registration_Nbr,
    Ext_Marking:row.Ext_Marking,
    shipname:row.shipname,
    shipname_norm:shipname_norm,
    Port_Code:row.Port_Code,
    Port_Name:row.Port_Name,
    callsign:row.callsign,
    IRCS:row.IRCS,
    Vms_Code:row.Vms_Code,
    Gear_Main_Code:row.Gear_Main_Code,
    Gear_Sec_Code:row.Gear_Sec_Code,
    Loa:row.Loa,
    Lbp:row.Lbp,
    Ton_Ref:row.Ton_Ref,
    Ton_Gt:row.Ton_Gt,
    Ton_Oth:row.Ton_Oth,
    Ton_Gts:row.Ton_Gts,
    Power_Main:row.Power_Main,
    Power_Aux:row.Power_Aux,
    Hull_Material:row.Hull_Material,
    Com_Year:row.Com_Year,
    Com_Month:row.Com_Month,
    Com_Day:row.Com_Day,
    Segment:row.Segment,
    Exp_Country:row.Exp_Country,
    Exp_Type:row.Exp_Type,
    Public_Aid_Code:row.Public_Aid_Code,
    Decision_Date:row.Decision_Date,
    Decision_Seg_Code:row.Decision_Seg_Code,
    Construction_Year:row.Construction_Year,
    Construction_Place:row.Construction_Place
  });
}



bigquery.defineFunction(
  'normalize_EU',  // Name of the function exported to SQL
  
  ['row_number','Country_Code','CFR','Event_Code','Event_Start_Date','Event_End__ate','License_Ind',
   'Registration_Nbr','Ext_Marking','shipname','Port_Code','Port_Name','callsign','IRCS','Vms_Code',
   'Gear_Main_Code','Gear_Sec_Code','Loa','Lbp','Ton_Ref','Ton_Gt','Ton_Oth','Ton_Gts','Power_Main','Power_Aux','Hull_Material',
   'Com_Year','Com_Month','Com_Day','Segment','Exp_Country','Exp_Type','Public_Aid_Code','Decision_Date',
   'Decision_Seg_Code','Construction_Year','Construction_Place'],  // Names of input columns
  
  [{'name':'row_number','type':'integer'},
  {'name':'Country_Code','type':'string'},
  {'name':'CFR','type':'string'},
  {'name':'Event_Code','type':'string'},
  {'name':'Event_Start_Date','type':'string'},
  {'name':'Event_End__ate','type':'string'},
  {'name':'License_Ind','type':'string'},
  {'name':'Registration_Nbr','type':'string'},
  {'name':'Ext_Marking','type':'string'},
  {'name':'shipname','type':'string'},
  {'name':'shipname_norm','type':'string'},
  {'name':'Port_Code','type':'string'},
  {'name':'Port_Name','type':'string'},
  {'name':'callsign','type':'string'},
  {'name':'IRCS','type':'string'},
  {'name':'Vms_Code','type':'string'},
  {'name':'Gear_Main_Code','type':'string'},
  {'name':'Gear_Sec_Code','type':'string'},
  {'name':'Loa','type':'float'},
  {'name':'Lbp','type':'float'},
  {'name':'Ton_Ref','type':'float'},
  {'name':'Ton_Gt','type':'float'},
  {'name':'Ton_Oth','type':'float'},
  {'name':'Ton_Gts','type':'float'},
  {'name':'Power_Main','type':'float'},
  {'name':'Power_Aux','type':'float'},
  {'name':'Hull_Material','type':'string'},
  {'name':'Com_Year','type':'string'},
  {'name':'Com_Month','type':'string'},
  {'name':'Com_Day','type':'string'},
  {'name':'Segment','type':'string'},
  {'name':'Exp_Country','type':'string'},
  {'name':'Exp_Type','type':'string'},
  {'name':'Public_Aid_Code','type':'string'},
  {'name':'Decision_Date','type':'string'},
  {'name':'Decision_Seg_Code','type':'string'},
  {'name':'Construction_Year','type':'string'},
  {'name':'Construction_Place','type':'string'}],
  
  normalize_EU                       // Reference to JavaScript UDF
);




