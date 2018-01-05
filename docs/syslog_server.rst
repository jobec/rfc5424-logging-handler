Logstash and RFC5424
====================

Due to the structured format of an RFC5424 it's easy to parse at the receiving side.
Below is an example configuration for Logstash (part of the Elastic stack).

I'm interested in more example configurations for parsing RFC5424 with other syslog receivers.
If you happen to have such configuration, feel free to open a pull request to have it added.

.. code-block:: ruby

    input {
        udp {
            port => 514
            type => "rfc5424"
        }
    }
    filter {
        if [type] == "rfc5424" {
            grok {
                match => {
                    "message" => "<%{NONNEGINT:syslog_pri}>%{NONNEGINT:version}%{SPACE}(?:-|%{TIMESTAMP_ISO8601:syslog_timestamp})%{SPACE}(?:-|%{IPORHOST:hostname})%{SPACE}(?:%{SYSLOG5424PRINTASCII:program}|-)%{SPACE}(?:-|%{SYSLOG5424PRINTASCII:process_id})%{SPACE}(?:-|%{SYSLOG5424PRINTASCII:message_id})%{SPACE}(?:-|(?<structured_data>(\[.*?[^\\]\])+))(?:%{SPACE}%{GREEDYDATA:syslog_message}|)"
                }
                add_tag => [ "match" ]
            }
            if "match" in [tags] {
                syslog_pri {
                    remove_field => "syslog_pri"
                }
                date {
                    match => [ "syslog_timestamp", "ISO8601", "MMM dd HH:mm:ss", "MMM dd HH:mm:ss.SSS" ]
                    remove_field => "syslog_timestamp"
                }
                if [structured_data] {
                    ruby {
                        code => '
                            # https://github.com/logstash-plugins/logstash-input-syslog/issues/15#issuecomment-270367033
                            def extract_syslog5424_sd(syslog5424_sd)
                                sd = {}
                                syslog5424_sd.scan(/\[(?<element>.*?[^\\])\]/) do |element|
                                    data = element[0].match(/(?<sd_id>[^\ ]+)(?<sd_params> .*)?/)
                                    sd_id = data[:sd_id].split("@", 2)[0]
                                    sd[sd_id] = {}
                                    next if data.nil? || data[:sd_params].nil?
                                    data[:sd_params].scan(/ (.*?[=](?:""|".*?[^\\]"))/) do |set|
                                        set = set[0].match(/(?<param_name>.*?)[=]\"(?<param_value>.*)\"/)
                                        sd[sd_id][set[:param_name]] = set[:param_value]
                                    end
                                end
                                sd
                            end
                            event.set("[sd]", extract_syslog5424_sd(event.get("[structured_data]")))
                        '
                        remove_field => "structured_data"
                    }
                }
            }
        }
    }
    output {
        elasticsearch {
            hosts => ["localhost:9200"]
            index => "rfc5424-%{+YYYY.MM.dd}"
        }
    }
