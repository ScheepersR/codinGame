use std::io;
use std::collections::HashMap;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

fn dereference_arg(arg: &str, spreadsheet: &[(String, String, String)], evaluations: &mut HashMap<usize, i32>) -> i32{
    if arg.starts_with("$"){
        let cell = arg.replace("$","").parse::<usize>().unwrap();
        evaluate(cell, spreadsheet, evaluations)
    } else if arg.starts_with("_"){
        0
    } else {
        arg.parse::<i32>().unwrap()
    }
}

fn evaluate(n: usize, spreadsheet: &[(String, String, String)], evaluations: &mut HashMap<usize, i32>) -> i32{
    let (op, arg_1, arg_2) = &spreadsheet[n];
    
    if evaluations.contains_key(&n){
        *evaluations.get(&n).unwrap()
    } else {
        let arg_1 = dereference_arg(&arg_1, spreadsheet, evaluations);
        let arg_2 = dereference_arg(&arg_2, spreadsheet, evaluations);
    
        let result = match op.as_str() {
            "VALUE" => arg_1,
            "ADD" => arg_1 + arg_2,
            "SUB" => arg_1 - arg_2,
            "MULT" => arg_1*arg_2,
            _ => panic!("Unexpected Operator")
        };
        evaluations.insert(n, result);
        result
    }
}

fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let n = parse_input!(input_line, i32);

    let mut spreadsheet = Vec::<(String, String, String)>::new();

    for _i in 0..n as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(" ").collect::<Vec<_>>();
        let operation = inputs[0].trim().to_string();
        let arg_1 = inputs[1].trim().to_string();
        let arg_2 = inputs[2].trim().to_string();
        spreadsheet.push((operation, arg_1, arg_2))
    }

    let mut evaluations = HashMap::new();

    for i in 0..n as usize {
        let x = evaluate(i, spreadsheet.as_slice(), &mut evaluations);
        println!("{}", x);
    }
}
