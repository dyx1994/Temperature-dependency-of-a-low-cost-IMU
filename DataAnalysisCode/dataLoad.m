function [ax, ay, az, gx, gy, gz, temperature] = dataLoad(filename)
    data_array = csvread(filename,1);
    ax = data_array(:,1);
    ay = data_array(:,2);
    az = data_array(:,3);
    gx = data_array(:,4)*180/3.14159;
    gy = data_array(:,5)*180/3.14159;
    gz = data_array(:,6)*180/3.14159;
    temperature = data_array(:,7);
end
