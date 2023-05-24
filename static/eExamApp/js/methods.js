


let option_count;

function set_defult_val(defult_value){
    option_count=Number(defult_value);
}

function add_options(option_ID,answer_id){

var option=document.getElementById(option_ID);
var answer=document.getElementById(answer_id);



    options_list_texts=new Array();
    var op;

    if(option_ID=='options_add')
    {
        for(var i=1;i<=option_count;i++){
            op=document.getElementById('op_text'+String(i)).value;
            options_list_texts.push(op);
        }    
    }
    else{
        for(var i=1;i<=option_count;i++){
            op=document.getElementById('e_op_text'+String(i)).value;
            options_list_texts.push(op);
            alert(option_count);
        } 

    }
    alert(option_count);

    option_count+=1;
    alert(option_count);
    if(option_ID=='options_add')
    {

        option.innerHTML+='<div class="row" id="op'+option_count+'"><div class="col-1">'+
        '<label for="no" class="form-label" style="background: #e2e9eb; width: 62px;height: 39px;font-size: 21px;text-align: center;">'+ option_count+'</label></div>'+
                '<div class="col-11"> <input name="op'+option_count+'" id="op_text'+option_count+'" class="form-control" list="datalistOptions" ></div></div>';
                for(var i=1;i<option_count;i++){
                    op=document.getElementById('op_text'+String(i));
                    op.value=options_list_texts[i-1];
                    
                }
             

         answer.innerHTML+='<div class="col-2" id="inlineRadio'+option_count+'"> <br><div class="form-check form-check-inline">'+
           '<input class="form-check-input" type="radio" name="inlineRadioOptions"  value="'+ option_count+'">'+
           '<label class="form-check-label" for="inlineRadio1">'+ option_count+'</label></div></div>';       
   
    }
    else{
        option.innerHTML+='<div class="row" id="e_op'+option_count+'"><div class="col-1">'+
        '<label for="no" class="form-label" style="background: #e2e9eb; width: 62px;height: 39px;font-size: 21px;text-align: center;">'+ option_count+'</label></div>'+
                '<div class="col-11"> <input name="e_op'+option_count+'" id="e_op_text'+option_count+'" class="form-control" list="datalistOptions" ></div></div>';
                for(var i=1;i<option_count;i++){
                    op=document.getElementById('e_op_text'+String(i));
                    op.value=options_list_texts[i-1];
                    
                }
             

         answer.innerHTML+='<div class="col-2" id="e_inlineRadio'+option_count+'"> <br><div class="form-check form-check-inline">'+
           '<input class="form-check-input" type="radio" name="inlineRadioOptions"  value="'+ option_count+'">'+
           '<label class="form-check-label" for="inlineRadio1">'+ option_count+'</label></div></div>';       
        
    }
   
 }

        
function delete_options(){
    if(option_count==1){
        alert('لا يمكن حذف هذا الصف');
    }
    else{
        var delete_option=document.getElementById('op'+String(option_count));
        var delete_answe=document.getElementById('inlineRadio'+String(option_count));
        delete_option.remove();
        delete_answe.remove();
        option_count--;
    }


    }

function get_model(model_name){
    $(document).ready(function(){
        $(model_name).modal('show');
    });
}