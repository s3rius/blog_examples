use std::collections::HashMap;
use std::fs::File;
use std::io;
use std::io::BufRead;

use pyo3::prelude::*;

/// Parse log file in rust.
/// This function parses log file and returns HashMap with Strings as keys and
/// Tuple of two u128 as values.
#[pyfunction]
fn parse_rust(filename: &str) -> PyResult<HashMap<String, (u128, u128)>> {
    let mut result_map = HashMap::new();
    // Iterating over file.
    for log in io::BufReader::new(File::open(filename)?).lines().flatten() {
        // Splitting log string.
        if let Ok(mut spl) = shell_words::split(&log) {
            // Getting file id.
            let file_id_opt = spl.get_mut(2).and_then(|http_req| {
                // Splitting method and URL.
                http_req.split(' ').into_iter().nth(1).and_then(|url| {
                    // Splitting by / and getting the last split.
                    url.split('/')
                        .into_iter()
                        .last()
                        // Split file id and extension.
                        .and_then(|item_url| item_url.split('.').into_iter().next())
                        // Turning &str into String.
                        .map(String::from)
                })
            });
            // Getting number of bytes sent.
            let bytes_sent_opt =
                spl.get_mut(4)
                    // Parsing string to u128
                    .and_then(|bytes_str| match bytes_str.parse::<u128>() {
                        Ok(bytes_sent) => Some(bytes_sent),
                        Err(_) => None,
                    });
            if file_id_opt.is_none() || bytes_sent_opt.is_none() {
                continue;
            }
            let file_id = file_id_opt.unwrap();
            let bytes_sent = bytes_sent_opt.unwrap();

            match result_map.get(&file_id) {
                Some(&(downloads, total_bytes_sent)) => {
                    result_map.insert(file_id, (downloads + 1, total_bytes_sent + bytes_sent));
                }
                None => {
                    result_map.insert(file_id, (1, bytes_sent));
                }
            }
        }
    }
    Ok(result_map)
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn rusty_log_parser(_py: Python, m: &PyModule) -> PyResult<()> {
    // Adding function to the module.
    m.add_function(wrap_pyfunction!(parse_rust, m)?)?;
    Ok(())
}
