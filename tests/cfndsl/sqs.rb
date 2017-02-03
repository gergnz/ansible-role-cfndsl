#!/usr/bin/env ruby

CloudFormation do

  params = {}
  external_parameters.each_pair do |key, val|
    key = key.to_s
    params[key] = val
  end

  Parameter('Queuename') do
    Type String
  end

  SQS_Queue('queue') do
    QueueName Ref('Queuename')
    DelaySeconds params['delay'] ||= 5
  end

  Output('Queue') do
    Value Ref('queue')
    Export 'Queue'
  end

end

