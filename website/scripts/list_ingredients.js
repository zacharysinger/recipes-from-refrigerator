var UIController = function(){

    var DOMString = {
        addInput: '.question',
        taskListContainer: '.result__list',
        listTask: '.list__task',
        taskText: '.list__task--text',
        editBtn: '.list__task--edit',
        delBtn: '.list__task--del'
    }

    return{
        testUI: function(){
            console.log('Call from UI');
        },

        getDOMString: function(){
            return DOMString;
        },

        getInput: function(){
            return document.querySelector(DOMString.addInput).value;
        },

        clearInput: function(){
            return document.querySelector(DOMString.addInput).value = "";
        },
        addTaskList: function(tasks){

            var html, markup, element;

            //Create HTML string with placeholder text
                element = DOMString.taskListContainer;

                html = '<li class="list__task" id="task-%id%"><button class="list__task--check" id="check"><i class="ion-ios-checkmark"></i></button><div class="list__task--text">%description%</div><button class="list__task--del" id="del"><i class="ion-android-delete"></i></button></li>';

            //replace the placeholder with some actual data
                markup = html.replace('%id%', tasks.id);
                markup = markup.replace('%description%', tasks.description);

            //Insert HTML into the DOM
                document.querySelector(element).insertAdjacentHTML("afterbegin", markup);
        },

        deleteTaskList: function(id){
            var el = document.getElementById("task-"+id);
            el.parentNode.removeChild(el);
        },

    }
}();


// ---------- Model Module ----------
// Concept: Create Formula, Calculate, Return Result
var TodolistController = function(){
    //Array Storage
    var data = [];

    //Task Instance for create new Item
    var Task = function(id, description){
        this.id = id,
        this.description = description
    }

    return{
        testModel: function(){
            console.log('Call from Model');
        },

        createNewTask:function(desc){
            var addItem, ID;

            if(data.length > 0){
                for(var i = 0; i < data.length; i++){
                    ID = i + 1;
                    addItem = new Task(ID, desc);
                }
            }else{
                ID = 0;
                addItem = new Task(ID, desc);
            }

            data.push(addItem);

            return addItem;
        },

        deleteTask: function(id){
            var ids, index;
            // Note : if you delete one of array, the index ref id will change
            // you have to solve this problem
            ids = data.map(function(current){
                return current.id;
            });

            //Part Delete
            index = ids.indexOf(parseInt(id));
            if(index !== -1){
                data.splice(index, 1);
            }
        }

    }
}();

// ---------- Controll ----------
// Concept : Parse Value, Check Event
var MainController = function(TodoCtrl,UICtrl){

    var setupEventListener = function(){
        var DOM = UICtrl.getDOMString();

        //Add(2) : Press Enter to Save
        document.querySelector(DOM.addInput).addEventListener('keypress', function(e){
            if(e.keyCode == 13 || e.which === 13){
                ctrlAdd();
            }
        });

        document.querySelector(DOM.taskListContainer).addEventListener('click', ctrlEventCheck);
    }

    //----------------------------------------------------

    var ctrlAdd = function(){
        var item;
        //1. Get value from input
        item = UICtrl.getInput();
        //2. Check Value
        if(item !== "" && item !== " "){
            //3. push value to array --> return tasks array
            var tasks = TodoCtrl.createNewTask(item);
            //4. update UI & clear input
            UICtrl.addTaskList(tasks);
            UICtrl.clearInput();
        }
    }

    //----------------------------------------------------
    //check ID from Event Delegation
    var ctrlEventCheck = function(event){
        var itemID, itemClass, IdSplit, ID;

        itemID = event.target.parentNode.parentNode.id;
        itemClass = event.target.parentNode.id;

        IdSplit = itemID.split("-");

        ID = IdSplit[1];

        if(itemClass === 'check'){
            UICtrl.checkedTaskList(ID);
        }else if(itemClass === 'del'){
            TodoCtrl.deleteTask(ID);
            UICtrl.deleteTaskList(ID);
        };
    }

    $('.clear_button').click(function() {
    $('ul').empty()
    });

    return{
        init: function(){
            console.log('script.js : connecting..');
            setupEventListener();
        }
    }
}(TodolistController,UIController);

MainController.init();
